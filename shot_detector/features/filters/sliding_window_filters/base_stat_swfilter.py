# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six
from functools import partial


from ..base_math_filter import BaseMathFilter
from .base_swfilter import BaseSWFilter




class BaseStatSWFilter(BaseSWFilter, BaseMathFilter):
    
    __logger = logging.getLogger(__name__)

    @staticmethod
    def get_max(features, max_key=lambda x : x, **kwargs):
        m = max(features, key=max_key)
        return m

    @staticmethod
    def get_min(features, min_key=lambda x : x, **kwargs):
        m = min(features, key=min_key)
        return m

    def get_mean(self, features, **kwargs):
        mean_function = self.choose_mean(**kwargs)
        mean_value = mean_function(features, **kwargs)
        return mean_value

    def choose_mean(self, mean_name = None, **kwargs):
        mean_function = self.get_average
        if 'weighted moving average' == mean_name or 'WMA' == mean_name:
            mean_function = self.get_wma
        elif 'exponentially weighted moving average' == mean_name or 'EWMA' == mean_name:
            mean_function = self.get_ewma
        elif 'gaussian weighted moving average' == mean_name or 'GWMA' == mean_name:
            mean_function = self.get_gwma
        elif 'median' == mean_name:
            mean_function = self.get_median
        return mean_function

    @staticmethod
    def get_median(features, sort_key=None, norm_function = None, **kwargs):
        if norm_function:
            sort_fun = partial(norm_function, **kwargs)
            sort_key = lambda x: sort_fun(x)[0]
        sorts = sorted(features, key=sort_key)
        length = int(len(sorts))
        if not length % 2:
            return (sorts[length // 2] + sorts[length // 2 - 1]) / 2.0
        return sorts[length // 2]

    @staticmethod
    def get_average(features, **kwargs):
        features_len = len(features)

        average = 1.0 * sum(features) / features_len


        return average

    def get_wma(self, features, **kwargs):
        """
            weighted moving average
        """
        n = len(features)
        if(n > 2):
            weighted_sum = 0
            for i, feature in enumerate(features):
                weighted_sum += feature * (n - i)
            weighted_average = 2 * weighted_sum / (n * (n - 1))
            return weighted_average
        return self.get_mean(features)

    def get_ewma(self, features, alpha=None, **kwargs):
        """
            exponentially weighted moving average
        """
        n = len(features)
        if None == alpha:
            alpha = 2 / (n + 1)
        if features:
            head = features[0]
            rest = self.get_ewma(features[1:], alpha, **kwargs)
            exponentially_weighted_average = alpha * head + (1 - alpha) * rest
            return exponentially_weighted_average
        return 0

    def get_gwma(self, features, **kwargs):
        """
            gaussian weighted moving average
        """
        gaussian_convolution = self.gaussian_convolve(features, **kwargs)
        return gaussian_convolution

    def get_deviation(self, features, std_coeff=3, *args, **kwargs):

        mean_value = self.get_mean(
            features=features,
            **kwargs
        )
        std_value = self.get_std(
            features=features,
            mean_value=mean_value,
            **kwargs
        )
        deviation = mean_value + std_value * std_coeff
        return deviation

    def get_std_error(self, features, mean_value=None, **kwargs):
        features_len = 1.0 * len(features)
        standard_deviation = self.get_std(
            features=features,
            mean_value=mean_value,
            **kwargs
        )
        standard_error = standard_deviation / self.sqrt(features_len)
        return standard_error

    def get_std(self, features, mean_value=None, **kwargs):
        corrected_variance = self.get_corrected_variance(
            features=features,
            mean_value=mean_value,
            **kwargs
        )
        standard_deviation_value = self.sqrt(corrected_variance)
        return standard_deviation_value

    def get_corrected_variance(self, features, mean_value=None, **kwargs):
        """
        Compute corrected sample variance.

        :param features: list_like
            list of samples.
        :param mean_value:
            precomputed mean value, if None mean will be computed/
        :param args:
            options for function `get_mean`
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
        corrected_variance = features_len * uncorrected_variance / (features_len - 1)
        return corrected_variance


    def get_uncorrected_variance(self, features, mean_value=None, **kwargs):
        """
        Compute uncorrected sample variance.

        :param features: list_like
            list of samples.
        :param mean_value:
            precomputed mean value, if None mean will be computed/
        :param args:
            options for function `get_mean`
        :param kwargs:
            options for function `get_mean`
        :return: sₙ² = E[(x - E[x])²]
             uncorrected sample variance
        """
        if None == mean_value:
            mean_value = self.get_mean(features, **kwargs)
        features_len = 1.0 * len(features)
        sum_list = []
        for feature in features:
            diff = feature - mean_value
            sum_list += [diff * diff]
        uncorrected_variance = self.get_mean(sum_list, **kwargs)
        return uncorrected_variance



