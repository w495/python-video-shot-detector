# -*- coding: utf8 -*-

from __future__ import absolute_import


import logging
import collections

import pprint
import six
import inspect
import av
from av.video.frame import VideoFrame
from av.video.stream import VideoStream
from av.audio.stream import AudioStream



from .utils import SmartDict, get_objdata_dict, TimeState


from .log_meta import LogMeta

class BasePositionState(SmartDict):
    prev = None
    curr = None


class BaseShotState(SmartDict):
    features        = BasePositionState()
    times           = BasePositionState()
    memory_cache    = SmartDict()
    opts            = SmartDict()
    shot_list       = []

class BaseDetector(six.with_metaclass(LogMeta, SmartDict)):

    logger = logging.getLogger(__name__)


    def detect(self, video_file_name, shot_state = None, *args, **kwargs):
        shot_state = self.handle_video(video_file_name, shot_state, *args, **kwargs)
        return shot_state

    def handle_video(self, video_file_name, shot_state = None, *args, **kwargs):
        shot_state = self.init_shot_state(shot_state, *args, **kwargs)
        video_container = av.open(video_file_name)
        if (self.logger.isEnabledFor(logging.INFO)):
            self.logger.debug("%s"%(video_container))
            self.log_tree(
                get_objdata_dict(
                    video_container,
                    ext_classes_keys = ['format', 'layout']
                )
            )
        shot_state = self.handle_video_container(video_container, shot_state, *args, **kwargs)
        return shot_state

    def log_tree(self, value, level = 1, *args, **kwargs):
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
                self.logger.debug("%s %s:"%(space, key))
                self.log_tree(value, level = level + 1)
            else:
                self.logger.debug("%s %s: %s"%(space, key, value))

    def handle_video_container(self, video_container, shot_state = None, *args, **kwargs):
        packet_list = video_container.demux()
        shot_state = self.handle_packet_list(packet_list, shot_state, *args, **kwargs)
        return shot_state

    def handle_packet_list(self, packet_list, shot_state = None, *args, **kwargs):
        for packet in packet_list:
            shot_state = self.handle_packet(packet, shot_state, *args, **kwargs)
        return shot_state

    def handle_packet(self, packet, shot_state = None, *args, **kwargs):
        frame_list = packet.decode()
        for frame in frame_list:
            shot_state = self.handle_frame(frame, shot_state, *args, **kwargs)
        return shot_state

    def handle_frame(self, frame, shot_state = None, *args, **kwargs):
        if(type(frame) == VideoFrame):
            shot_state = self.handle_videoframe(frame, shot_state, *args, **kwargs)
        return shot_state

    def handle_videoframe(self, frame, shot_state = None, *args, **kwargs):
        shot_state.features.prev = shot_state.features.curr
        shot_state.features.curr, shot_state = self.get_features(frame, shot_state, *args, **kwargs)
        shot_state.times.prev = shot_state.times.curr
        shot_state.times.curr = TimeState(frame.time)
        shot_state = self.handle_features(shot_state.features, shot_state, *args, **kwargs)
        return shot_state

    def get_features(self, frame, shot_state = None, *args, **kwargs):
        image,    shot_state = self.build_image(frame, shot_state)
        image,    shot_state = self.transform_image(image, shot_state)
        features, shot_state = self.build_features(image, shot_state)
        features, shot_state = self.transform_features(features, shot_state)
        return features, shot_state

    def init_shot_state(self, shot_state = None, *args, **kwargs):
        if shot_state:
            return self.build_shot_state(**shot_state)
        return self.build_shot_state(
            options = SmartDict(*args, **kwargs)
        )

    def build_shot_state(self, *args, **kwargs):
        return BaseShotState(
            detector_options = self,
            *args, **kwargs
        )

    def handle_features(self, features, shot_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return shot_state

    def build_image(self, frame, shot_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return frame, shot_state

    def transform_image(self, image, shot_state = None, *args, **kwargs):
        image, shot_state = self.transform_image_size(image, shot_state)
        image, shot_state = self.transform_image_colors(image, shot_state)
        return image, shot_state

    def transform_image_size(self, image, shot_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return image, shot_state

    def transform_image_colors(self, image, shot_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return image, shot_state


    def build_features(self, image, shot_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return image, shot_state

    def transform_features(self, features, shot_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return features, shot_state

    def get_colour_size(self):
        return 1 << 8

    def get_pixel_size(self):
        return self.get_colour_size() * 3


