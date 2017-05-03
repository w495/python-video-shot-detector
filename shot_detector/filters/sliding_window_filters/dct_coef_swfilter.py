# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from scipy.fftpack import dct

from .base_stat_swfilter import BaseStatSWFilter


class DCTCoefSWFilter(BaseStatSWFilter):
    """
        Implements 1D Fast Discrete COS transform.
        Only for experiment.
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self, window_seq, coef=0, **kwargs):
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
            spectrum = dct(window)
            yield list(spectrum)[coef] / (2 * wlen)
