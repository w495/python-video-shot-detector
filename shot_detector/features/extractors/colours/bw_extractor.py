# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from ..base_extractor import BaseExtractor


from shot_detector.utils.numerical import threshold_otsu


class BwExtractor(BaseExtractor):

    def build_image(self, frame, video_state, *args, **kwargs):
        image, video_state = self.frame_to_image(frame, 'rgb24', video_state)
        image, video_state = self.convert_to_luminosity(image, video_state, *args, **kwargs)
        otsu_vector = threshold_otsu(image)
        otsu_vector = self.normalize_colour(otsu_vector, video_state, *args, **kwargs)
        return otsu_vector, video_state
