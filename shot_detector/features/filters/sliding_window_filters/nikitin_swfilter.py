# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .min_std_regression_swfilter import MinStdRegressionSWFilter

class NikitinSWFilter(MinStdRegressionSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):

        for window in window_seq:
            x_window = self.split(window, depth=depth)
            for index, item in enumerate(x_window):
                if index == 0:
                    yield -0.1
                else:
                    yield item
