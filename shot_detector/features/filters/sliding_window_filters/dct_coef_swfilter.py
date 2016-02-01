# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from scipy.fftpack import dct, dst, idct, idst


from .stat_swfilter import StatSWFilter

import math

class DCTCoefSWFilter(StatSWFilter):
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

            yield list(spectrum)[0] / (2*wlen)

