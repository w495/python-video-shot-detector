# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from ..base_math_filter import BaseMathFilter
from .base_swfilter import BaseSWFilter


class BaseStatSWFilter(BaseSWFilter, BaseMathFilter):
    
    __logger = logging.getLogger(__name__)

    def get_max(self, features, max_key=None, *args, **kwargs):
        m = max(features, key=max_key)
        return m

    def get_mean(self, features, *args, **kwargs):
        mean_function = self.choose_mean(*args, **kwargs)
        mean_value = mean_function(features, *args, **kwargs)
        return mean_value

    def choose_mean(self, *args, **kwargs):
        mean_name = kwargs.pop('mean_name', None)
        mean_function = self.get_average
        if('weighted average' == mean_name or 'wa' == mean_name):
            mean_function = self.get_wa
        elif('exponentially weighted average' == mean_name or 'ewa' == mean_name):
            mean_function = self.get_ewa
        elif('gaussian weighted average' == mean_name or 'gwa' == mean_name):
            mean_function = self.get_gwa
        elif('median' == mean_name):
            mean_function = self.get_median
        return mean_function
    
    def get_median(self, features, sort_key=None, *args, **kwargs):
        sorts = sorted(features, key=sort_key)
        length = int(len(sorts))
        if not length % 2:
            return (sorts[length // 2] + sorts[length // 2 - 1]) / 2.0
        return sorts[length // 2]
    
    def get_average(self, features, *args, **kwargs):
        features_len = len(features)
        average = sum(features) / features_len
        return average

    def get_wa(self, features, *args, **kwargs):
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

    def get_ewa(self, features, alpha=None, *args, **kwargs):
        """
            exponentially weighted moving average
        """
        n = len(features)
        if None == alpha:
            alpha = 2 / (n + 1)
        if features:
            head = features[0]
            rest = self.get_ewa(features[1:], alpha, *args, **kwargs)
            exponentially_weighted_average = alpha * head + (1 - alpha) * rest
            return exponentially_weighted_average
        return 0

    def get_gwa(self, features, *args, **kwargs):
        """
            gaussian weighted moving average
        """
        n = len(features)
        gaussian_features = self.gaussian_features(features, *args, **kwargs)
        mean = self.get_mean(gaussian_features)
        return mean

    def get_deviation(self, features, std_coeff=3, *args, **kwargs):
        mean_value = self.get_mean(
            features=features,
            *args, **kwargs
        )
        std_value = self.get_std(
            features=features,
            mean_value=mean_value,
            *args, **kwargs
        )
        deviation = mean_value + std_value * std_coeff
        return deviation

    def get_std_error(self, features, mean_value=None, *args, **kwargs):
        features_len = 1.0 * len(features)
        standard_deviation = self.get_std(
            features=features,
            mean_value=mean_value,
            *args, **kwargs
        )
        standard_error = standard_deviation / self.sqrt(features_len)
        return standard_error

    def get_std(self, features, mean_value=None, *args, **kwargs):
        corrected_variance = self.get_corrected_variance(
            features=features,
            mean_value=mean_value,
            *args, **kwargs
        )

        standard_deviation_value = self.sqrt(corrected_variance)
        return standard_deviation_value

    def get_corrected_variance(self, features, mean_value=None, *args, **kwargs):
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
            *args, **kwargs
        )

        if 1 == features_len:
            features_len = 2

        corrected_variance = features_len * uncorrected_variance / (features_len - 1)


        return corrected_variance


    def get_uncorrected_variance(self, features, mean_value=None, *args, **kwargs):
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
            mean_value = self.get_mean(features, *args, **kwargs)
        features_len = 1.0 * len(features)
        sum_list = []
        for feature in features:
            diff = feature - mean_value
            sum_list += [diff * diff]
        uncorrected_variance = self.get_mean(sum_list, *args, **kwargs)
        return uncorrected_variance



