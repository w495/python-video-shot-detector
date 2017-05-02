# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class DixonRangeSWFilter(BaseStatSWFilter):
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.

            Sets the minimal size for sliding window.
            It is important for computing the gap:
                n = len(y) - 1
                gap = (y[n] - y[n - j])
        """

        min_size = 2

    def aggregate_window_item(self,
                              window,
                              number_of_outliers=1,
                              test_min=False,
                              **kwargs):
        sorted_window = self.get_sorted(window, **kwargs)
        y = list(sorted_window)
        n = len(y) - 1
        sorted_gap = (y[n] - y[n - number_of_outliers])
        if test_min:
            sorted_gap = (y[0] - y[number_of_outliers])
        sorted_range = (y[n] - y[number_of_outliers])
        dixon_range = sorted_gap / sorted_range
        return dixon_range
