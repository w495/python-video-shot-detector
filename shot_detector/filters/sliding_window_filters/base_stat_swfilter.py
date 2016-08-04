# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
from functools import partial

from scipy import stats

from .base_swfilter import BaseSWFilter
from ..math_filter import MathFilter


class BaseStatSWFilter(BaseSWFilter, MathFilter):
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
        m = min(features, key=min_key)
        return m

    def get_mean(self, features, **kwargs):
        mean_function = self.choose_mean(**kwargs)
        mean_value = mean_function(features, **kwargs)
        return mean_value

    # noinspection PyUnusedLocal
    def choose_mean(self, mean_name=None, **_kwargs):
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
    def get_sorted(features, sort_key=None,
                   norm_function=None, **kwargs):
        if norm_function:
            sort_fun = partial(norm_function, **kwargs)
            sorts = sorted(features, key=lambda x: sort_fun(x)[0])
        else:
            sorts = sorted(features, key=sort_key)
        return sorts

    def get_median(self, features, **kwargs):
        sorts = self.get_sorted(features, **kwargs)
        length = int(len(sorts))
        if not length % 2:
            return (sorts[length // 2] + sorts[length // 2 - 1]) / 2.0
        return sorts[length // 2]

    # noinspection PyUnusedLocal
    @staticmethod
    def get_average(features, **_kwargs):
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
        n = len(features)
        if alpha is None:
            alpha = 2 / (n + 1)
        rest = self.get_ewma_rest(features, alpha, n, **kwargs)
        return rest

    def get_ewma_rest(self, features, alpha=None, n=0, **kwargs):
        """
            exponentially weighted moving average
            :param features:
            :param alpha:
        """
        head = features[-1]
        rest = features[:-1]
        if n <= 1:
            return head
        rest = self.get_ewma_rest(rest, alpha, n - 1, **kwargs)
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
        corrected_variance = features_len * uncorrected_variance / (
        features_len - 1)
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

    def describe(self, features, **kwargs):
        return stats.describe(features)



        #
        #
        # cdef inline DTYPE_t median3(DTYPE_t* Xf, SIZE_t n) nogil:
        #     # Median of three pivot selection, after Bentley and McIlroy (1993).
        #     # Engineering a sort function. SP&E. Requires 8/3 comparisons on average.
        #     cdef DTYPE_t a = Xf[0], b = Xf[n / 2], c = Xf[n - 1]
        #     if a < b:
        #         if b < c:
        #             return b
        #         elif a < c:
        #             return c
        #         else:
        #             return a
        #     elif b < c:
        #         if a < c:
        #             return a
        #         else:
        #             return c
        #     else:
        #         return b
        #
