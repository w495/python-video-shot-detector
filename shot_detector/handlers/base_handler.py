# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

import av

from shot_detector.objects          import SmartDict, BaseVideoState
from shot_detector.utils.common     import get_objdata_dict
from shot_detector.utils.log_meta   import LogMeta

class BaseHandler(six.with_metaclass(LogMeta, SmartDict)):
    '''
        Finite State Machine for video handling.
        Works with video at law level.
        Splits video into frames.
        You should implement `handle_frame` method.
    '''

    __logger = logging.getLogger(__name__)

    def handle_video(self, video_file_name, video_state = None, *args, **kwargs):
        video_state = self.init_video_state(video_state, *args, **kwargs)
        video_container = av.open(video_file_name)
        logger = self.__logger
        if (logger.isEnabledFor(logging.INFO)):
            logger.debug("%s"%(video_container))
            self.log_tree(
                logger,
                get_objdata_dict(
                    video_container,
                    ext_classes_keys = ['format', 'layout']
                )
            )
        video_state = self.handle_video_container(
            video_container, 
            video_state, 
            *args, 
            **kwargs
        )
        return video_state

    def log_tree(self, logger, value, level = 1, *args, **kwargs):
        space = ' ⇾ ' * level
        for key, value in six.iteritems(value):
            if isinstance(value, dict):
                xtype = value.get('type')
                if(xtype):
                    key += " [%s]"%str(xtype)
                name = value.get('name')
                if(name):
                    key += " {%s} "%str(name)
                long_name = value.get('long_name')
                if(long_name):
                    key += " «%s»"%str(long_name)
                logger.debug("%s %s:"%(space, key))
                self.log_tree(logger, value, level = level + 1)
            else:
                logger.debug("%s %s: %s"%(space, key, value))

    def handle_video_container(self, video_container, video_state = None, *args, **kwargs):
        packet_list = video_container.demux()
        video_state = self.handle_packet_list(
            packet_list, 
            video_state, 
            *args, 
            **kwargs
        )
        return video_state

    def handle_packet_list(self, packet_list, video_state = None, *args, **kwargs):
        for packet_number, packet in enumerate(packet_list):
            ## For debug we save information about packet.
            video_state.packet_number = packet_number
            video_state.packet = packet
            video_state = self.handle_packet(
                packet, 
                video_state, 
                *args, 
                **kwargs
            )
        return video_state

    def handle_packet(self, packet, video_state = None, *args, **kwargs):
        frame_list = packet.decode()
        for frame_number, frame in enumerate(frame_list):
            ## For debug we save information about frame.
            video_state.frame_number = frame_number
            video_state.frame = frame
            video_state = self.handle_frame(
                frame, 
                video_state, 
                *args, 
                **kwargs
            )
        return video_state

    def init_video_state(self, video_state = None, *args, **kwargs):
        if video_state:
            return self.build_video_state(**video_state)
        return self.build_video_state(
            options = SmartDict(*args, **kwargs)
        )

    def build_video_state(self, *args, **kwargs):
        '''
            Creates internal state for Finite State Machine.
            If you want to change state-class, you have to
            overload this method.
        '''
        return BaseVideoState(
            detector_options = self,
            *args, **kwargs
        )

    def handle_frame(self, frame, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return video_state
