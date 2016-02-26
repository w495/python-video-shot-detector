# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from numpy.polynomial import polynomial


from shot_detector.utils.numerical import gaussian_1d_convolve
from .filter import Filter


class MathFilter(Filter):
    __logger = logging.getLogger(__name__)

    EPSILON = np.finfo(float).eps

    # noinspection PyUnusedLocal
    @staticmethod
    def simple_histogram(features, bins=10, **_kwargs):
        hist, _ = np.histogram(features, bins=bins)
        return hist

    @staticmethod
    def bool(expression, **kwargs):
        use_any = kwargs.pop('use_any', False)
        out_expression = np.array(expression)
        if use_any:
            return out_expression.any()
        return out_expression.all()

    # noinspection PyUnusedLocal
    @staticmethod
    def to_vector(expression, **_kwargs):
        return np.array(expression)

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
    def sqrt(expression, **_kwargs):
        return np.sqrt(expression)

    def escape_null(self, expression):
        return expression + self.EPSILON

    # noinspection PyUnusedLocal
    def log(self, expression, **_kwargs):
        expr = self.escape_null(expression)
        return np.log(expr)

    # noinspection PyUnusedLocal
    def exp(self, expression, **_kwargs):
        expr = self.escape_null(expression)
        return np.exp(expr)

    # noinspection PyUnusedLocal
    def log10(self, expression, **_kwargs):
        expr = self.escape_null(expression)
        return np.log10(expr)

    # noinspection PyUnusedLocal
    def polynomial(self, x, y=None, order=2, **_kwargs):
        if y is None:
            y = x
        coef = polynomial.polyfit(x, y, order)
        value = polynomial.polyval(x, coef)
        return value



