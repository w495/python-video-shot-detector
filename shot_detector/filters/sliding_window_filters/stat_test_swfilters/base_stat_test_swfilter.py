# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from scipy import stats

from ..base_stat_swfilter import BaseStatSWFilter


class BaseStatTestSWFilter(BaseStatSWFilter):
    __logger = logging.getLogger(__name__)

    def normaltest(self, features, **kwargs):
        return stats.normaltest(features)

    def ttest_ind(self, features1, features2, **kwargs):
        return stats.ttest_ind(features1, features2, **kwargs)

    def ttest_rel(self, features1, features2, **kwargs):
        """
        Calculates the T-test on TWO RELATED
        samples of scores, a and b.

        This is a two-sided test for the null hypothesis
        that 2 related or repeated samples
        have identical average (expected) values.
        """
        return stats.ttest_rel(features1, features2, **kwargs)

    def ranksums(self, features1, features2, **_):
        return stats.ranksums(features1, features2)

    def ks_2samp(self, features1, features2, **_):
        return stats.ks_2samp(features1, features2)

    def mannwhitneyu(self, features1, features2, **kwargs):
        return stats.mannwhitneyu(features1, features2, **kwargs)
