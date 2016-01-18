# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class DecisionTreeRegressorSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)

    # noinspection PyUnusedLocal
    @staticmethod
    def aggregate_window(window_features, window_state, **_kwargs):
        return window_features, window_state
