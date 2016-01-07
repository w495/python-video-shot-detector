# -*- coding: utf8 -*-

from __future__ import absolute_import

from ..base_extractor import BaseExtractor


class RgbExtractor(BaseExtractor):

    def build_image(self, frame, **kwargs):
        image, video_state = self.frame_to_image(frame, 'rgb24')
        return image
