# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
from functools import partial

from scipy import stats

from shot_detector.filters.common import MathFilter

from .base_swfilter import BaseSWFilter


class BaseStatSWFilter(BaseSWFilter, MathFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    # noinspection PyUnusedLocal
    @staticmethod
    def get_max(features, max_key=lambda x: x, **_kwargs):
        """
        Returns native max of given sequence of features.

        :param collections.Iterable[Feature] features:
            sequence of features
        :param lambda max_key:
        :param _kwargs:
        :return:
        """
        m = max(features, key=max_key)
        return m

    # noinspection PyUnusedLocal
    @staticmethod
    def get_min(features, min_key=lambda x: x, **_kwargs):
        """
        
        :param features: 
        :param min_key: 
        :param _kwargs: 
        :return: 
        """
        m = min(features, key=min_key)
        return m

    def get_mean(self, features, **kwargs):
        """
        
        :param features: 
        :param kwargs: 
        :return: 
        """
        mean_function = self.choose_mean(**kwargs)
        mean_value = mean_function(features, **kwargs)
        return mean_value

    # noinspection PyUnusedLocal
    def choose_mean(self, mean_name=None, **_kwargs):
        """
        
        :param mean_name: 
        :param _kwargs: 
        :return: 
        """
        mean_function = self.get_average
        # weighted moving average
        if 'WMA' == mean_name:
            mean_function = self.get_wma
        # exponentially weighted moving average
        elif 'EWMA' == mean_name:
            mean_function = self.get_ewma
        # gaussian weighted moving average
        elif 'GWMA' == mean_name:
            mean_function = self.get_gwma
        elif 'median' == mean_name:
            mean_function = self.get_median
        return mean_function

    @staticmethod
    def get_sorted(features, sort_key=None,
                   norm_function=None, **kwargs):
        """
        
        :param features: 
        :param sort_key: 
        :param norm_function: 
        :param kwargs: 
        :return: 
        """
        if norm_function:
            sort_fun = partial(norm_function, **kwargs)
            sorts = sorted(features, key=lambda x: sort_fun(x)[0])
        else:
            sorts = sorted(features, key=sort_key)
        return sorts

    def get_median(self, features, **kwargs):
        """
        
        :param features: 
        :param kwargs: 
        :return: 
        """
        sorts = self.get_sorted(features, **kwargs)
        length = int(len(sorts))
        if not length % 2:
            return (sorts[length // 2] + sorts[length // 2 - 1]) / 2.0
        return sorts[length // 2]

    # noinspection PyUnusedLocal
    @staticmethod
    def get_average(features, **_kwargs):
        """
        
        :param features: 
        :param _kwargs: 
        :return: 
        """
        features_len = len(features)
        average = 1.0 * sum(features) / features_len
        return average

    # noinspection PyUnusedLocal
    def get_wma(self, features, **_kwargs):
        """
            weighted moving average
            :param features:
        """
        n = len(features)
        if n > 1:
            weighted_sum = 0
            for i, feature in enumerate(features):
                weighted_sum += feature * (n - i - 1)
            weighted_average = 2 * weighted_sum / (n * (n - 1))
            return weighted_average
        return self.get_mean(features)

    def get_ewma(self, features, alpha=None, **kwargs):
        """
            exponentially weighted moving average
            :param features:
            :param alpha:
        """
        if not features:
            return 0
        features = list(features)
        size = len(features)
        if alpha is None:
            alpha = 2 / (size + 1)
        rest = self.get_ewma_rest(features, alpha, size, **kwargs)
        return rest

    def get_ewma_rest(self, features, alpha=None, size=0, **kwargs):
        """
            exponentially weighted moving average
            :param features:
            :param int alpha:
            :param int size:
            :param kwargs
        """
        head = features[-1]
        rest = features[:-1]
        if size <= 1:
            return head
        rest = self.get_ewma_rest(rest, alpha, size - 1, **kwargs)
        ewa = alpha * head + (1 - alpha) * rest
        return ewa

    def get_gwma(self, features, **kwargs):
        """
            gaussian weighted moving average
            :param features:
        """
        gaussian_convolution = self.gaussian_convolve(features,
                                                      **kwargs)
        return gaussian_convolution

    def get_deviation(self, features, std_coef=3, **kwargs):
        """
        
        :param features: 
        :param std_coef: 
        :param kwargs: 
        :return: 
        """
        mean_value = self.get_mean(
            features=features,
            **kwargs
        )
        std_value = self.get_std(
            features=features,
            mean_value=mean_value,
            **kwargs
        )
        deviation = mean_value + std_value * std_coef
        return deviation

    def get_mad(self, features, **kwargs):
        """
        Mean absolute deviation

        :param features:
        :param kwargs:
        :return:
        """

        features_len = 1.0 * len(features)
        mean_value = self.get_mean(
            features=features,
            **kwargs
        )
        mad_sum = 0.0
        for feature in features:
            mad_sum += abs(feature - mean_value)
        deviation = 1.0 * (mad_sum / features_len)
        return deviation

    def get_std_error(self, features, mean_value=None, **kwargs):
        """
            Computes SE_x = std / sqrt(n)

            See https://en.wikipedia.org/wiki/Standard_error

        :param features:
        :param mean_value:
        :param kwargs:
        :return:
        """
        features_len = 1.0 * len(features)
        standard_deviation = self.get_std(
            features=features,
            mean_value=mean_value,
            **kwargs
        )
        standard_error = standard_deviation / self.sqrt(features_len)
        return standard_error

    def get_std(self, features, mean_value=None, **kwargs):
        """
            Computes corrected sample standard deviation

        :param features:
        :param mean_value:
        :param kwargs:
        :return:
        """
        corrected_variance = self.get_corrected_variance(
            features=features,
            mean_value=mean_value,
            **kwargs
        )
        standard_deviation_value = self.sqrt(corrected_variance)
        return standard_deviation_value

    def get_corrected_variance(self, features, mean_value=None,
                               **kwargs):
        """
        Compute corrected sample variance.

        :param features: list_like
            list of samples.
        :param mean_value:
            precomputed mean value, if None mean will be computed/
        :param kwargs:
            options for function `get_mean`
        :return: s² = (n /(n - 1)) * sₙ²  =  (n /(n - 1)) E[(x - E[x])²]
             uncorrected sample variance
        """
        features_len = 1.0 * len(features)
        uncorrected_variance = self.get_uncorrected_variance(
            features=features,
            mean_value=mean_value,
            **kwargs
        )
        if 1 == features_len:
            features_len = 2
        corrected_variance = \
            features_len * uncorrected_variance / (features_len - 1)
        return corrected_variance

    def get_uncorrected_variance(self, features, mean_value=None,
                                 **kwargs):
        """
        Compute uncorrected sample variance.

        :param features: list_like
            list of samples.
        :param mean_value:
            precomputed mean value, if None mean will be computed/
        :param kwargs:
            options for function `get_mean`
        :return: sₙ² = E[(x - E[x])²]
             uncorrected sample variance
        """
        if mean_value is None:
            mean_value = self.get_mean(features, **kwargs)
        sum_list = []
        for feature in features:
            diff = feature - mean_value
            sum_list += [diff * diff]
        uncorrected_variance = self.get_mean(sum_list, **kwargs)
        return uncorrected_variance

    @staticmethod
    def describe(features, **_):
        """
        
        :param features: 
        :param _: 
        :return: 
        """
        return stats.describe(features)
