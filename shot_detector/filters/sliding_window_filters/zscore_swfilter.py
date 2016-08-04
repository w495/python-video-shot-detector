# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class ZScoreSWFilter(BaseStatSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self,
                              window,
                              null_std=0,
                              sigma_num=0,
                              **kwargs):
        mean = self.get_mean(window, **kwargs)
        std = self.get_std(window, mean, **kwargs)
        feature = window[-1]

        if self.bool(std == 0, **kwargs):
            return null_std
        z_score = abs((feature - mean) / self.escape_null(std))
        greater = (z_score > sigma_num)
        return greater
