# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

import numpy as np

from .math_filter import MathFilter


class ColourFilter(MathFilter):
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self,
                            feature,
                            **kwargs):
        return self.extract_item_colour(feature, **kwargs)

    @staticmethod
    def extract_item_colour(feature,
                            pattern=None,
                            y=None,
                            cr=None,
                            cb=None,
                            red=0,
                            green=0,
                            blue=0,
                            summand=0,
                            factor=1,
                            **_kwargs):

        if y is not None:
            pattern = (299, 587, 114)
            summand = 0
            factor = y

        if cr is not None:
            pattern = (500000, -418688, -81312)
            summand = 0.5
            factor = cr

        if cb is not None:
            pattern = (-168736, -331264, 500000)
            summand = 0.5
            factor = cb

        if pattern is None:
            pattern = (red, green, blue)

        psum = sum(pattern)
        ypbpr = np.inner(feature, pattern) / psum
        result = summand + factor * ypbpr
        return result
