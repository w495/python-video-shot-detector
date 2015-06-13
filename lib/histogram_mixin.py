# -*- coding: utf8 -*-

from __future__ import absolute_import


class HistogramMixin(object):

    def build_features(self, image, shot_state = None):
        histogram_vector = image.histogram()
        return histogram_vector, shot_state
