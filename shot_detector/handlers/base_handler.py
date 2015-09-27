# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import av
import six

import datetime

from shot_detector.utils.collections import SmartDict

from shot_detector.objects import BaseVideoState, BaseFrame
from shot_detector.utils.common import get_objdata_dict
from shot_detector.utils.log_meta import LogMeta


class BaseHandler(six.with_metaclass(LogMeta)):
    """
        Finite State Machine for video handling.
        Works with video at law level.
        Splits video into frames.
        You should implement `handle_frame` method.
    """

    __logger = logging.getLogger(__name__)

    def handle_video(self, video_file_name, video_state=None, *args, **kwargs):
        video_state = self.init_video_state(video_state, *args, **kwargs)
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
        video_state = self.handle_video_container(
            video_container,
            video_state,
            *args,
            **kwargs
        )
        return video_state

    def log_tree(self, logger, value, level=1, *args, **kwargs):
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

    def handle_video_container(self, video_container, video_state, *args, **kwargs):
        packet_list = video_container.demux()
        video_state = self.handle_packet_list(
            packet_list,
            video_state,
            *args,
            **kwargs
        )
        return video_state

    def handle_packet_list(self, packet_list, video_state, *args, **kwargs):
        for packet_number, raw_packet in enumerate(packet_list):
            video_state = self.handle_packet(
                # For debug we save information about packet.
                SmartDict(
                    global_number=packet_number,
                    source=raw_packet,
                ),
                video_state,
                *args,
                **kwargs
            )
        return video_state

    def handle_packet(self, packet, video_state, *args, **kwargs):
        frame_list = packet.source.decode()
        packet_number = packet.global_number
        for frame_number, raw_frame in enumerate(frame_list):
            video_state.counters.frame += 1
            video_state = self.handle_frame(
                # For debug we save information about frame.
                BaseFrame(
                    time=raw_frame.time,
                    source=raw_frame,
                    global_number=video_state.counters.frame,
                    frame_number = frame_number,
                    packet_number = packet_number,
                ),
                video_state,
                *args,
                **kwargs
            )
        return video_state

    def init_video_state(self, video_state, *args, **kwargs):
        if video_state:
            return self.build_video_state(**video_state)
        return self.build_video_state(
            options=SmartDict(*args, **kwargs)
        )

    def build_video_state(self, *args, **kwargs):
        """
            Creates internal state for Finite State Machine.
            If you want to change state-class, you have to
            overload this method.
        """
        return BaseVideoState(
            start_datetime = datetime.datetime.now(),
            *args, **kwargs
        )

    def handle_frame(self, frame, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return video_state
