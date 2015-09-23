# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

import numpy as np

from .base_stat_swfilter import BaseStatSWFilter

class DeviationSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window(self, window_features, window_state, *args, **kwargs):
        deviation = self.get_deviation(window_features, *args, **kwargs)
        return deviation, window_state

