# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .scipy_stat_swfilter import SciPyStatSWFilter





class KolmogorovSmirnov2SamplesTestSwfilter(SciPyStatSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):

        prev_win = None
        for window in window_seq:
            if prev_win is None:
                prev_win = window

            result = self.ks_2samp(prev_win, window)
            print (result)

            yield result.pvalue
            prev_win = window
