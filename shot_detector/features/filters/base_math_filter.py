# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from shot_detector.utils.numerical import gaussian_1d_convolve
from .base_filter import BaseFilter


class BaseMathFilter(BaseFilter):
    __logger = logging.getLogger(__name__)

    EPSILON = np.finfo(float).eps

    # noinspection PyUnusedLocal
    @staticmethod
    def get_simple_histogram(features, bins=10, **_kwargs):
        hist, _ = np.histogram(features, bins=bins)
        return hist

    @staticmethod
    def bool(expresion, **kwargs):
        use_any = kwargs.pop('use_any', False)
        out_expresion = np.array(expresion)
        if use_any:
            return out_expresion.any()
        return out_expresion.all()

    # noinspection PyUnusedLocal
    @staticmethod
    def to_vector(expresion, **_kwargs):
        return np.array(expresion)

    # noinspection PyUnusedLocal
    @staticmethod
    def gaussian_convolve(features, gaussian_sigma=None, **_kwargs):
        """
            gaussian_features = gaussian_1d (feature)
            :param features:
            :param gaussian_sigma:
        """
        convolution = gaussian_1d_convolve(
            vector=features,
            sigma=gaussian_sigma,
        )
        result = sum(convolution)
        return result

    # noinspection PyUnusedLocal
    @staticmethod
    def sqrt(expresion, **_kwargs):
        return np.sqrt(expresion)

    def escape_null(self, expresion):
        return expresion + self.EPSILON

    # noinspection PyUnusedLocal
    def log(self, expresion, **_kwargs):
        expr = self.escape_null(expresion)
        return np.log(expr)

    # noinspection PyUnusedLocal
    def log10(self, expresion, **_kwargs):
        expr = self.escape_null(expresion)
        return np.log10(expr)
