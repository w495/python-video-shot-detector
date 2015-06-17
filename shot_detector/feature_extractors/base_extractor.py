# -*- coding: utf8 -*-

from __future__ import absolute_import

from shot_detector.detectors import BaseDetector

class BaseExtractor(BaseDetector):

    def extract_features(self, frame, video_state = None, *args, **kwargs):
        image,    video_state = self.build_image(frame, video_state)
        image,    video_state = self.transform_image(image, video_state)
        features, video_state = self.build_features(image, video_state)
        features, video_state = self.transform_features(features, video_state)
        return features, video_state

    def build_image(self, frame, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return frame, video_state

    def transform_image(self, image, video_state = None, *args, **kwargs):
        image, video_state = self.transform_image_size(image, video_state)
        image, video_state = self.transform_image_colors(image, video_state)
        return image, video_state


    def transform_image_size(self, image, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return image, video_state

    def transform_image_colors(self, image, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return image, video_state


    def build_features(self, image, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return image, video_state

    def transform_features(self, features, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return features, video_state

    def get_colour_size(self):
        return 1 << 8

    def get_pixel_size(self):
        return self.get_colour_size() * 3


