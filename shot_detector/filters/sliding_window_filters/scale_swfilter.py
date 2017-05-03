# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np
from sklearn import preprocessing

from .base_stat_swfilter import BaseStatSWFilter


class ScaleSWFilter(BaseStatSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          return_velocity=False,
                          **kwargs):

        min_max_scaler = preprocessing.MinMaxScaler()

        for window in window_seq:

            reshaped_window = np.array(window).reshape(-1, 1)
            window_scaled = min_max_scaler.fit_transform(
                reshaped_window)

            for win_index, win_item in enumerate(window_scaled):
                # if win_index == 0:
                yield win_item





                # def aggregate_windows(self,
                #                       window_seq,
                #                       return_velocity = False,
                #                       **kwargs):
                #
                #
                #     for window in window_seq:
                #
                #         window_scaled = savgol_filter(window,25,3)
                #
                #         for win_index, win_item in enumerate(window_scaled):
                #             #if win_index == 0:
                #             yield win_item
                #
