# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

import numpy as np

from .base_stat_swfilter import BaseStatSWFilter

class MedianSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window(self, window_features, window_state, *args, **kwargs):
        median = self.get_median(window_features)
        return median, window_state

