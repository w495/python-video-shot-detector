# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

import numpy as np

from .base_stat_swfilter import BaseStatSWFilter


class MeanSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)
    

    def aggregate_window(self, window_features, window_state, *args, **kwargs):
        mean = self.get_mean(window_features, *args, **kwargs)
        return mean, window_state

