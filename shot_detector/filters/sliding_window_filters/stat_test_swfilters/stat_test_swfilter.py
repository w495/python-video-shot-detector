# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_test_swfilter import BaseStatTestSWFilter


class StatTestSWFilter(BaseStatTestSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):
        prev_win = None
        for window in window_seq:
            if prev_win is None:
                prev_win = window
            result = self.ttest_rel(prev_win, window)
            print('result = ', result)

            yield result.pvalue
            prev_win = window
