# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from scipy.fftpack import dct, dst, idct, idst


from .stat_swfilter import StatSWFilter

import math

class FftSWFilter(StatSWFilter):
    """
        Implements 1D Fast Discrete COS transform.
        Only for experiment.
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self, window_seq, **kwargs):
        """
        Reduce sliding windows into values

        :param collections.Iterable[SlidingWindow] window_seq:
            sequence of sliding windows
        :param kwargs: ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]
        """


        for window in window_seq:
            wlen = len(window)
            coef = wlen
            spectrum = dct(window, type=2)

            print ('wlen  = ', wlen)

            yield list(spectrum)[1] / (2*wlen)

            # for win_index, win_item in enumerate(window):
            #     regression_item = sum(
            #         spec_item * np.cos(
            #             math.pi * (win_index + 0.5) * (spec_index) /
            #             (wlen)
            #         )
            #         for spec_index, spec_item in enumerate(
            #             spectrum[1:]
            #         )
            #     )
            #     if win_index == 0:
            #         yield 1
            #     else:
            #         yield regression_item / np.sqrt(wlen)
