# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime
import logging

import av
import six
# noinspection PyUnresolvedReferences
from av.container import InputContainer

from shot_detector.objects import (
    BaseFrame,
    FramePosition
)
from shot_detector.utils.common import get_objdata_dict
from shot_detector.utils.log_meta import (
    LogMeta,
    ignore_log_meta,
    should_be_overloaded
)


class BaseHandler(six.with_metaclass(LogMeta)):
    """
        Finite State Machine for video handling.
        Works with video at law level.
        Splits video into frames.
        You should implement `handle_frame` method.


    """

    __logger = logging.getLogger(__name__)

    def handle_video(self,
                     input_uri='',
                     format_name=None,
                     **kwargs):
        """
        Runs video handling

        :param str input_uri:
            file name of input video or path to resource
            for example `http://localhost:8090/live.flv`
            You can use any string, that can be accepted
            by input ffmpeg-parameter. For example:
                * 'udp://127.0.0.1:1234';
                * 'tcp://localhost:1234?listen';
                * 'http://localhost:8090/live.flv'.
        :param str format_name:
            name of video format. Use it for hardware devices.
        :param dict kwargs: any options for consecutive methods,
            ignores it and pass it through
        :return:
        """

        # noinspection PyUnresolvedReferences
        video_container = av.open(
            file=input_uri,
            format=format_name,
        )

        logger = self.__logger
        if logger.isEnabledFor(logging.INFO):
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
    def log_tree(self, logger, value, level=1, **_):
        """

        :param logging.Logger logger:
        :param Any value:
        :param int level:
        :param dict _: any options for consecutive methods,
            ignores it and pass it through
        :return:
        """
        space = ' ⇾ ' * level
        for key, value in six.iteritems(value):
            if isinstance(value, dict):
                type_ = value.get('type')
                if type_:
                    key += " [%s]" % str(type_)
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
        """
        :param av.container.InputContainer video_container:
            input video container, in terms of
            av open video file or stream.
        :param kwargs: any options for consecutive methods,
            ignores it and pass it through.
        :return:

        """
        assert isinstance(video_container, InputContainer)

        packet_seq = self.packets(video_container, **kwargs)
        packet_seq = self.filter_packets(packet_seq, **kwargs)
        frame_seq = self.frames(packet_seq, **kwargs)
        filtered_seq = self.filter_frames(frame_seq, **kwargs)
        handled_seq = self.handle_frames(filtered_seq, **kwargs)
        list(handled_seq)
        return None

    @staticmethod
    def packets(video_container, stream_seq=None, **_):
        """

        :param av.container.InputContainer video_container:
        :param stream_seq:
        :param _:
        :return:
        """
        if stream_seq:
            stream_seq = tuple(stream_seq)
        return video_container.demux(streams=stream_seq)

    @should_be_overloaded
    def filter_packets(self, packet_seq, **_):
        """

        :param collections.Iterable packet_seq:
        :param dict _: ignores it.
        :return:
        """
        return packet_seq

    @staticmethod
    def packet_frame_seqs(packet_seq, **_):
        """

        :param collections.Iterable packet_seq:
        :param dict _: ignores it.
        :return:
        """
        for packet in packet_seq:
            decoded = packet.decode()
            yield iter(decoded)

    def frames(self, packet_seq, **kwargs):
        """

        :param collections.Iterable packet_seq:
        :param dict kwargs: any options for consecutive methods,
            ignores it and pass it through.
        :return:
        """
        packet_frame_seqs = self.packet_frame_seqs(packet_seq, **kwargs)
        global_number = 0
        for packet_number, frame_seq in enumerate(packet_frame_seqs):
            for frame_number, source_frame in enumerate(frame_seq):
                position = FramePosition(
                    global_number=global_number,
                    frame_number=frame_number,
                    packet_number=packet_number,
                )
                frame = self.frame(
                    source=source_frame,
                    position=position,
                )
                yield frame
                global_number += 1

    def frame(self, source=None, position=None):
        """
        
        :param source: 
        :param position: 
        :return: 
        """

        frame = BaseFrame(
            av_frame=source,
            position=position,
        )
        return frame

    @should_be_overloaded
    def filter_frames(self, frame_seq, **_):
        """

        :param collections.Iterable frame_seq:
        :param dict _: ignores it.
        :return:
        """
        return frame_seq

    @should_be_overloaded
    def handle_frames(self, frame_seq, **_):
        """

        :param collections.Iterable frame_seq:
        :param dict _: ignores it..
        :return:
        """
        return frame_seq

    @staticmethod
    def limit_seq(sequence, first=0, last=10, as_stream=False, **_):
        """

        :param sequence:
        :param float first:
        :param float last:
        :param bool as_stream:
        :param _:
        :return:
        """

        at_start = None
        for unit in sequence:
            BaseHandler.__logger.debug('unit = %s', unit)

            current = float(unit.time)
            if as_stream:
                if at_start is None:
                    at_start = current
                current = current - at_start

            if last <= current:
                sequence.close()
            if first <= current:
                yield unit

    def log_seq(self,
                sequence,
                fmt="[{delta_time}] {item}",
                logger=None,
                log=None,
                **kwargs):
        """
        Prints sequence item by item

        :param sequence:
        :param fmt:
        :param logger:
        :param log:
        :param kwargs:
        :return:
        """
        start_time = datetime.datetime.now()

        if logger is None:
            logger = logging.getLogger(__name__)
        if log is None:
            log = logger.info

        if fmt is None:
            fmt = "WRONG FORMAT …"

        for item in sequence:
            now_time = datetime.datetime.now()
            delta_time = now_time - start_time
            item_dict = kwargs
            for attr in dir(item):
                if not attr.startswith('__'):
                    item_dict['item.{}'.format(attr)] \
                        = getattr(item, attr)
            log(fmt.format(
                delta_time=delta_time,
                self=self,
                item=item,
                **item_dict
            ))
            yield item
