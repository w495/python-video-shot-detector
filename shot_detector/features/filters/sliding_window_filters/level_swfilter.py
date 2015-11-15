# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

import numpy as np

from .base_stat_swfilter import BaseStatSWFilter


class LevelSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)


    def aggregate_window_item(self, window_features, level_number=8, **kwargs):
        max = self.get_max(window_features, **kwargs)
        min = self.get_min(window_features, **kwargs)
        width = (max + min)
        bin_width = width / level_number
        res = 0
        current = window_features[0]
        for step in xrange(level_number):
            left = min + bin_width * step
            right = min + bin_width * (step + 1)
            if left <= current <= right:
                res = step / level_number
                break
        return res

