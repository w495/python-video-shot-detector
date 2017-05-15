# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from .base_stat_swfilter import BaseStatSWFilter


class PearsonCorrelationSWFilter(BaseStatSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          return_velocity=False,
                          **kwargs):
        """
        
        :param window_seq: 
        :param return_velocity: 
        :param kwargs: 
        :return: 
        """

        prev_window = None
        for window in window_seq:
            if not prev_window:
                prev_window = window
                yield window[0]
            else:
                prev_window_arr = np.array(prev_window)
                window_arr = np.array(window)
                yield np.corrcoef([
                    prev_window_arr,
                    window_arr
                ])[0, 1]
                prev_window = window
