# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
from builtins import range

from scipy.fftpack import dct, idct

from .base_stat_swfilter import BaseStatSWFilter


class DCTLinearRegressorSWFilter(BaseStatSWFilter):
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
            window_len = len(window)
            coef = window_len
            spectrum = dct(window)
            inverse_spectrum = idct(spectrum[:coef])
            for item in inverse_spectrum:
                result = item / (2 * window_len)
                for _ in range(window_len // coef):
                    yield result
