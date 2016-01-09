# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import datetime
import logging

import av
import six

from shot_detector.objects import BaseFrame
from shot_detector.utils.common import get_objdata_dict
from shot_detector.utils.log_meta import LogMeta, ignore_log_meta, should_be_overloaded


class BaseHandler(six.with_metaclass(LogMeta)):
    """
        Finite State Machine for video handling.
        Works with video at law level.
        Splits video into frames.
        You should implement `handle_frame` method.
    """

    __logger = logging.getLogger(__name__)

    def handle_video(self, video_file_name, **kwargs):
        video_container = av.open(video_file_name)
        logger = self.__logger
        if logger.isEnabledFor(logging.INFO):
            logger.info("%s" % video_container)
            self.log_tree(
                logger,
                get_objdata_dict(
                    video_container,
                    ext_classes_keys=['format', 'layout']
                )
            )

        result = self.handle_video_container(video_container, **kwargs)
        return result

    # noinspection PyUnusedLocal
    @ignore_log_meta
    def log_tree(self, logger, value, level=1, **_kwargs):
        space = ' ⇾ ' * level
        for key, value in six.iteritems(value):
            if isinstance(value, dict):
                xtype = value.get('type')
                if xtype:
                    key += " [%s]" % str(xtype)
                name = value.get('name')
                if name:
                    key += " {%s} " % str(name)
                long_name = value.get('long_name')
                if long_name:
                    key += " «%s»" % str(long_name)
                logger.info("%s %s:" % (space, key))
                self.log_tree(logger, value, level=level + 1)
            else:
                logger.info("%s %s: %s" % (space, key, value))

    def handle_video_container(self, video_container, **kwargs):
        packet_seq = self.packets(video_container, **kwargs)
        packet_seq = self.filter_packets(packet_seq, **kwargs)
        frame_seq = self.frames(packet_seq, **kwargs)
        filtered_seq = self.filter_frames(frame_seq, **kwargs)
        handled_seq = self.handle_frames(filtered_seq, **kwargs)
        list(handled_seq)
        return None

    # noinspection PyUnusedLocal
    @staticmethod
    def packets(video_container, stream_seq=None, **_kwargs):
        if stream_seq:
            stream_seq = tuple(stream_seq)
        return video_container.demux(streams=stream_seq)

    @should_be_overloaded
    def filter_packets(self, packet_seq, **_kwargs):
        return packet_seq

    # noinspection PyUnusedLocal
    @staticmethod
    def packet_frame_seqs(packet_seq, **_kwargs):
        for packet in packet_seq:
            yield iter(packet.decode())

    def frames(self, packet_seq, **kwargs):
        """
        :type packet_seq: __generator[int]


        """
        packet_frame_seqs = self.packet_frame_seqs(packet_seq, **kwargs)
        global_number = 0
        for packet_number, frame_seq in enumerate(packet_frame_seqs):
            for frame_number, source_frame in enumerate(frame_seq):
                frame = self.frame(source_frame, global_number, frame_number, packet_number)
                yield frame
                global_number += 1

    def frame(self, source, global_number, frame_number, packet_number):
        frame = BaseFrame(
            source=source,
            global_number=global_number,
            frame_number=frame_number,
            packet_number=packet_number,
        )
        self.__logger.debug(frame)
        return frame

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def filter_frames(self, frame_seq, **_kwargs):
        return frame_seq

    @should_be_overloaded
    def handle_frames(self, frame_seq, **_kwargs):
        return frame_seq


