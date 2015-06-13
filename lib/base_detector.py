# -*- coding: utf8 -*-

from __future__ import absolute_import

import logging

from six import with_metaclass

import av
from av.video.frame import VideoFrame

from .utils import SmartDict


from .log_meta import LogMeta

class BasePositionState(object):
    prev = None
    curr = None

class BaseShotState(object):
    features = BasePositionState()
    times    = BasePositionState()
    memory_cache = SmartDict()

#with_metaclass(LogMeta)

class BaseDetector(object):

    def detect(self, video_file_name, shot_state = None):
        shot_state = self.handle_video(video_file_name, shot_state)
        return shot_state

    def handle_video(self, video_file_name, shot_state = None):
        video_container = av.open(video_file_name)
        shot_state = self.handle_video_container(video_container, shot_state)
        return shot_state

    def handle_video_container(self, video_container, shot_state = None):
        packet_list = video_container.demux()
        shot_state = self.handle_packet_list(packet_list, shot_state)
        return shot_state

    def handle_packet_list(self, packet_list, shot_state = None):
        shot_state = self.init_shot_state(shot_state)
        for packet in packet_list:
            shot_state = self.handle_packet(packet, shot_state)
        return shot_state

    def handle_packet(self, packet, shot_state = None):
        frame_list = packet.decode()
        for frame in frame_list:
            shot_state = self.handle_frame(frame, shot_state)
        return shot_state

    def handle_frame(self, frame, shot_state = None):
        if(type(frame) == VideoFrame):
            shot_state = self.handle_videoframe(frame, shot_state)
        return shot_state

    def handle_videoframe(self, frame, shot_state = None):
        shot_state.features.prev = shot_state.features.curr
        shot_state.features.curr, shot_state = self.get_features(frame, shot_state)
        shot_state.times.prev = shot_state.times.curr
        shot_state.times.curr = frame.time
        shot_state = self.handle_features(shot_state.features, shot_state)
        return shot_state

    def get_features(self, frame, shot_state = None):
        frame_image, shot_state = self.build_image(frame, shot_state)
        frame_image, shot_state = self.transform_image(frame_image, shot_state)
        features,    shot_state = self.build_features(frame_image, shot_state)
        features,    shot_state = self.transform_features(features, shot_state)
        return features, shot_state

    def init_shot_state(self, shot_state = None):
        if shot_state:
            return shot_state
        return self.build_shot_state()

    def build_shot_state(self):
        return BaseShotState()

    def handle_features(self, features, shot_state = None):
        '''
            Should be implemented
        '''
        return shot_state

    def build_image(self, frame, shot_state = None):
        '''
            Should be implemented
        '''
        return None, shot_state

    def transform_image(self, image, shot_state = None):
        image, shot_state = self.transform_image_size(image, shot_state)
        image, shot_state = self.transform_image_colors(image, shot_state)
        return image, shot_state

    def transform_image_size(self, image, shot_state = None):
        '''
            Should be implemented
        '''
        return image, shot_state

    def transform_image_colors(self, image, shot_state = None):
        '''
            Should be implemented
        '''
        return image, shot_state


    def build_features(self, image, shot_state = None):
        '''
            Should be implemented
        '''
        return None, shot_state

    def transform_features(self, features, shot_state = None):
        '''
            Should be implemented
        '''
        return features, shot_state





