# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

import numpy as np

from .base_stat_swfilter import BaseStatSWFilter


from sklearn.tree import DecisionTreeRegressor

class DecisionTreeRegressorSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window(self, window_features, window_state, level_number = 2, *args, **kwargs):


        return window_features, window_state

