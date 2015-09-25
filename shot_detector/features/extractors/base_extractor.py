# -*- coding: utf8 -*-

from __future__ import absolute_import

from shot_detector.handlers import BaseFrameHandler


class BaseExtractor(BaseFrameHandler):

    def extract_features(self, frame, video_state=None, *args, **kwargs):
        image, video_state = self.build_image(frame, video_state)
        image, video_state = self.transform_image(image, video_state)
        features, video_state = self.build_features(image, video_state)
        features, video_state = self.transform_features(features, video_state)
        if(not video_state.pixel_size):
            video_state.pixel_size, video_state = self.get_pixel_size(
                image,
                video_state,
                *args,
                **kwargs
            )
        if(not video_state.colour_size):
            video_state.colour_size, video_state = self.get_colour_size(
                image,
                video_state,
                *args,
                **kwargs
            )

        return features, video_state

    def build_image(self, frame, video_state=None, *args, **kwargs):
        """
            Should be implemented
        """
        return frame, video_state

    def transform_image(self, image, video_state=None, *args, **kwargs):
        image, video_state = self.transform_image_size(image, video_state)
        image, video_state = self.transform_image_colors(image, video_state)
        return image, video_state


    def transform_image_size(self, image, video_state=None, *args, **kwargs):
        """
            Should be implemented
        """
        return image, video_state

    def transform_image_colors(self, image, video_state=None, *args, **kwargs):
        """
            Should be implemented
        """
        return image, video_state


    def build_features(self, image, video_state=None, *args, **kwargs):
        """
            Should be implemented
        """
        return image, video_state

    def transform_features(self, features, video_state=None, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state

    def get_colour_size(self, image, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return 1, video_state

    def get_raw_pixel_size(self, image, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return 1, video_state


    def get_pixel_size(self, image, video_state, *args, **kwargs):
        pixel_size, video_state = self.get_raw_pixel_size(image, video_state, *args, **kwargs)
        return pixel_size, video_state
   

