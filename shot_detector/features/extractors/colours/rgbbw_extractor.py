# -*- coding: utf8 -*-

from __future__ import absolute_import

from shot_detector.utils.numerical import threshold_otsu
from ..base_extractor import BaseExtractor


class RgbBwExtractor(BaseExtractor):
    def build_image(self, frame, video_state, *args, **kwargs):
        image, video_state = self.frame_to_image(frame, 'rgb24', video_state)
        for i in xrange(image.shape[-1]):
            image[:, :, i] = threshold_otsu(image[:, :, i])
        # image, video_state = self.normalize_colour(image, video_state, *args, **kwargs)
        return image, video_state
