# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import math

import numpy as np
from scipy.fftpack import dct


from scipy.signal import detrend

from .stat_swfilter import StatSWFilter



from .min_std_regression_swfilter import MinStdRegressionSWFilter

class NikitinSWFilter(MinStdRegressionSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):

        for window in window_seq:
            x_window = self.split(window, depth=depth, **kwargs)
            for index, item in enumerate(x_window):
                yield item

                # if index == 0:
                #     yield -0.1
                # else:
                #     yield item

    def replace_items(self, sequence, replacer=None, **kwargs):


        values = list(self.extract_values(sequence))
        mean = self.get_mean(values, **kwargs)

        upper_values = list(
            item for item in values if item >= mean
        )
        lower_values = list(
            item for item in values if item < mean
        )


        print ('mean = ', mean)
        print ('values = ', values)
        print ('upper_values = ', upper_values)
        print ('lower_values = ', lower_values)

        diff = 0
        if lower_values and upper_values:
            upper_mean = self.get_mean(upper_values)
            lower_mean = self.get_mean(lower_values)
            diff = upper_mean - lower_mean


        for index, item in enumerate(sequence):
            if not item.state:
                yield self.Atom(
                    index=item.index,
                    value=diff,
                    state=True
                )
            else:
                yield item

