# -*- coding: utf8 -*-

from __future__ import absolute_import

from .base_image_mixin import BaseImageMixin

class HistogramImageMixin(BaseImageMixin):

    def build_features(self, image, shot_state = None, *args, **kwargs):
        histogram_vector = image.histogram()
        return histogram_vector, shot_state
