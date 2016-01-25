# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from .stat_swfilter import StatSWFilter


class FftSWFilter(StatSWFilter):
    """
        Implements 1D Fast Discrete Hartley transform.
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
            fft_spectrum = np.fft.fft(window)
            for fft_item in fft_spectrum:
                hartley_item = fft_item.real - fft_item.imag
                yield hartley_item

