# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from scipy.fftpack import dct, dst, idct, idst


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
            wlen = len(window)
            coef = 5
            fft_spectrum = dct(window)

            print ('fft_spectrum  =', fft_spectrum)

            ifft_spectrum = idct(fft_spectrum[:coef])


            print ('ifft_spectrum  =', ifft_spectrum)


            for fft_item in ifft_spectrum:
                hartley_item = fft_item

                for i in xrange(wlen // coef):
                    yield hartley_item / wlen



