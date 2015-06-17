# -*- coding: utf8 -*-

from __future__ import absolute_import

class Histogram(object):

    def build_features(self, image, video_state = None, *args, **kwargs):
        histogram_vector, video_state = self.colour_histogram(
            image,
            video_state
        )
        return histogram_vector, video_state

