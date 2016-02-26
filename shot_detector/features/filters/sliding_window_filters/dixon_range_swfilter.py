# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter

class DixonRangeSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self,
                              window,
                              number_of_outliers=1,
                              test_min=False,
                              **kwargs):
        sorted_window = self.get_sorted(window, **kwargs)
        y = list(sorted_window)
        n = len(y) - 1
        sorted_gap = (y[n] - y[n-number_of_outliers])
        if test_min:
            sorted_gap = (y[1] - y[number_of_outliers])
        sorted__range = (y[n] - y[number_of_outliers])
        dixon_range = sorted_gap/ sorted__range
        return dixon_range
