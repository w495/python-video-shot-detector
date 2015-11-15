# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import av
import six
import itertools

import datetime

from shot_detector.utils.collections import SmartDict

from shot_detector.objects import BaseVideoState, BaseFrame
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
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("%s" % (video_container))
            self.log_tree(
                logger,
                get_objdata_dict(
                    video_container,
                    ext_classes_keys=['format', 'layout']
                )
            )

        result = self.handle_video_container(video_container, **kwargs)
        return result

    @ignore_log_meta
    def log_tree(self, logger, value, level=1, **kwargs):
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
                logger.debug("%s %s:" % (space, key))
                self.log_tree(logger, value, level=level + 1)
            else:
                logger.debug("%s %s: %s" % (space, key, value))

    def handle_video_container(self, video_container, **kwargs):

        packet_iterable = self.packets(video_container, **kwargs)
        packet_iterable = self.filtrer_packets(packet_iterable, **kwargs)

        frame_iterable = self.frames(packet_iterable, **kwargs)
        frame_iterable = self.filter_frames(frame_iterable, **kwargs)

        handled_iterable = self.handle_frames(frame_iterable, **kwargs)
        list(handled_iterable)
        return None

    @staticmethod
    def packets(video_container, stream_iterable = None, **kwargs):
        if stream_iterable:
            stream_iterable = tuple(stream_iterable)
        return video_container.demux(streams=stream_iterable)

    def filtrer_packets(self, packet_iterable, **kwargs):
        self.__logger.debug('filtrer_packets: not implemented')
        return packet_iterable


    def packet_frame_iterables(self, packet_iterable, **kwargs):
        for packet in packet_iterable:
            yield iter(packet.decode())

    def frames(self, packet_iterable, **kwargs):
        packet_frame_iterables = self.packet_frame_iterables(packet_iterable, **kwargs)
        global_number = 0
        for packet_number, frame_iterable in enumerate(packet_frame_iterables):
            for frame_number, frame in  enumerate(frame_iterable):
                global_number +=1
                yield BaseFrame(
                    source=frame,
                    global_number=global_number,
                    frame_number=frame_number,
                    packet_number=packet_number,
                )

    @should_be_overloaded
    def filter_frames(self, frame_iterable, **kwargs):
        return frame_iterable

    @should_be_overloaded
    def handle_frames(self, frame_iterable, **kwargs):
        return frame_iterable

    def init_video_state(self, video_state, **kwargs):
        if video_state:
            return self.build_video_state(**video_state)
        return self.build_video_state(
            options=SmartDict(**kwargs)
        )

    @staticmethod
    def build_video_state(**kwargs):
        """
            Creates internal state for Finite State Machine.
            If you want to change state-class, you have to
            overload this method.
        """
        return BaseVideoState(
            start_datetime = datetime.datetime.now(),
            **kwargs
        )

