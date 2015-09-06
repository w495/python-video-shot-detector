# -*- coding: utf8 -*-

from __future__ import absolute_import

from ..base_extractor import BaseExtractor

class LumaExtractor(BaseExtractor):

    def build_image(self, frame, video_state, *args, **kwargs):
        image, video_state = self.frame_to_image(frame, 'rgb24', video_state)
        image, video_state = self.convert_to_luminosity(image, video_state, *args, **kwargs)
        return image, video_state
