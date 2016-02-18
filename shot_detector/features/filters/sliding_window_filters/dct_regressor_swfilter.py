# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import math

import numpy as np
from scipy.fftpack import dct

from .stat_swfilter import StatSWFilter


class DCTRegressorSWFilter(StatSWFilter):
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
            spec_slice = slice(0, 2)
            spectrum = dct(window, type=2)
            spectrum = spectrum[spec_slice]
            for win_index, win_item in enumerate(window):
                i_spectrum_chain = (
                    self.__norm(spec_index, wlen) * spec_item * np.cos(
                        math.pi * (2 * win_index - 1) * (spec_index) /
                        (2 * wlen)
                    )
                    for spec_index, spec_item in enumerate(
                    spectrum
                )
                )
                regression_item = 2 * sum(i_spectrum_chain)
                yield regression_item

    @staticmethod
    def __norm(p, wlen):
        x = 2 if 0 == p else 1
        return 1 / (2 * x * wlen)
