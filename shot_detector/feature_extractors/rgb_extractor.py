# -*- coding: utf8 -*-

from __future__ import absolute_import

from .base_extractor import BaseExtractor

class RgbExtractor(object):

    def build_image(self, frame, video_state):
        image, video_state = self.frame_to_image(frame, 'rgb24', video_state)
        return image, video_state
