# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from scipy import stats

from ..base_stat_swfilter import BaseStatSWFilter


class BaseStatTestSWFilter(BaseStatSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    @staticmethod
    def normal_test(features, **_):
        """
        
        :param features: 
        :param _: 
        :return: 
        """
        return stats.normaltest(features)

    @staticmethod
    def ttest_ind(features1, features2, **kwargs):
        """
        
        :param features1: 
        :param features2: 
        :param kwargs: 
        :return: 
        """
        return stats.ttest_ind(features1, features2, **kwargs)

    @staticmethod
    def ttest_rel(features1, features2, **kwargs):
        """
        Calculates the T-test on TWO RELATED
        samples of scores, a and b.

        This is a two-sided test for the null hypothesis
        that 2 related or repeated samples
        have identical average (expected) values.
        """
        return stats.ttest_rel(features1, features2, **kwargs)

    @staticmethod
    def rank_sums(features1, features2, **_):
        """
        
        :param features1: 
        :param features2: 
        :param _: 
        :return: 
        """
        return stats.ranksums(features1, features2)

    @staticmethod
    def ks_2samp(features1, features2, **_):
        """
        
        :param features1: 
        :param features2: 
        :param _: 
        :return: 
        """
        return stats.ks_2samp(features1, features2)

    @staticmethod
    def mannwhitneyu(features1, features2, **kwargs):
        """
        
        :param features1: 
        :param features2: 
        :param kwargs: 
        :return: 
        """
        return stats.mannwhitneyu(features1, features2, **kwargs)
