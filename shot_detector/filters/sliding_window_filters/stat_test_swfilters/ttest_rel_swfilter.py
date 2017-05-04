# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_test_swfilter import BaseStatTestSWFilter


class DependentStudentTtestSWFilter(BaseStatTestSWFilter):
    """
    Calculates the T-test on TWO RELATED samples of scores, a and b.

    This is a two-sided test for the null hypothesis
    that 2 related or repeated samples
    have identical average (expected) values.
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):
        """
        
        :param window_seq: 
        :param depth: 
        :param kwargs: 
        :return: 
        """
        prev_win = None
        for window in window_seq:
            if prev_win is None:
                prev_win = window
            result = self.ttest_rel(prev_win, window)
            yield result.pvalue
            prev_win = window
