# -*- coding: utf8 -*-

from __future__ import absolute_import

from ..base_extractor import BaseExtractor

class LongLumaExtractor(BaseExtractor):

    def build_image(self, frame, video_state, *args, **kwargs):
        image, video_state = self.frame_to_image(frame, 'gray16le', video_state)
        return image, video_state


