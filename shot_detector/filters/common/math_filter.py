# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
from builtins import range

import numpy as np
from numpy.polynomial import polynomial

from shot_detector.filters.dsl import DslPlainFilter
from shot_detector.utils.numerical import gaussian_1d_convolve


class MathFilter(DslPlainFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    EPSILON = np.finfo(float).eps

    # noinspection PyUnusedLocal
    @staticmethod
    def simple_histogram(features, bins=10, **_kwargs):
        """
        
        :param features: 
        :param bins: 
        :param _kwargs: 
        :return: 
        """
        hist, _ = np.histogram(features, bins=bins)
        return hist

    @staticmethod
    def bool(expression, use_any=False, **_):
        """
        
        :param expression: 
        :param use_any:
        :return: 
        """
        out_expression = np.array(expression)
        if use_any:
            return out_expression.any()
        return out_expression.all()

    # noinspection PyUnusedLocal
    @staticmethod
    def to_vector(expression, **_kwargs):
        """
        
        :param expression: 
        :param _kwargs: 
        :return: 
        """
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
        """
        
        :param expression: 
        :param _kwargs: 
        :return: 
        """
        return np.sqrt(expression)

    def escape_null(self, expression):
        """
        
        :param expression: 
        :return: 
        """
        return expression + self.EPSILON

    # noinspection PyUnusedLocal
    def log(self, expression, **_kwargs):
        """
        
        :param expression: 
        :param _kwargs: 
        :return: 
        """
        expr = self.escape_null(expression)
        return np.log(expr)

    # noinspection PyUnusedLocal
    def exp(self, expression, **_kwargs):
        """
        
        :param expression: 
        :param _kwargs: 
        :return: 
        """
        expr = self.escape_null(expression)
        return np.exp(expr)

    # noinspection PyUnusedLocal
    def log10(self, expression, **_kwargs):
        """
        
        :param expression: 
        :param _kwargs: 
        :return: 
        """
        expr = self.escape_null(expression)
        return np.log10(expr)

    # noinspection PyUnusedLocal
    @staticmethod
    def polynomial(values=None, numbers=None, order=2, **_kwargs):
        """
        
        :param values: 
        :param numbers: 
        :param order: 
        :param _kwargs: 
        :return: 
        """
        if numbers is None:
            numbers = range(len(values))
        coef = polynomial.polyfit(numbers, values, order)
        value = polynomial.polyval(numbers, coef)
        return value

    # noinspection PyUnusedLocal
    def polynomial_error(self, values=None, **kwargs):
        """
        
        :param values: 
        :param kwargs: 
        :return: 
        """
        poly_values = self.polynomial(values, **kwargs)
        diff_values = values - poly_values
        return diff_values
