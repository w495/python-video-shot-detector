# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from scipy.signal import savgol_filter

from .base_stat_swfilter import BaseStatSWFilter


class SavitzkyGolaySWFilter(BaseStatSWFilter):
    """
        Least-squares fit of a polynomial to data.

        A Savitzky–Golay filter is a digital filter that can be
        applied to a set of digital data points for the purpose of
        smoothing the data, that is, to increase the signal-to-noise
        ratio without greatly distorting the signal.

        This is achieved, in a process known as convolution,
        by fitting successive sub-sets of adjacent data points with
        a low-degree polynomial by the method of linear least
        squares. When the data points are equally spaced an
        analytical solution to the least-squares equations can be
        found, in the form of a single set of "convolution
        coefficients" that can be applied to all data sub-sets,
        to give estimates of the smoothed signal, (or derivatives of
        the smoothed signal) at the central point of each sub-set.
    """

    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.

            Sets the minimal size for sliding window.
        """

        min_size = 3

    def aggregate_windows(self,
                          window_seq,
                          polyorder=2,
                          **kwargs):

        for window in window_seq:
            wlen = len(window)
            if not wlen % 2:
                wlen -= 1
            if wlen < polyorder:
                polyorder = wlen - 1
            window_scaled = savgol_filter(
                window,
                wlen,
                polyorder
            )
            for win_index, win_item in enumerate(window_scaled):
                yield win_item
