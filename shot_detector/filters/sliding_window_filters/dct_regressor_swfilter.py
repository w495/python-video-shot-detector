# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import math

import numpy as np
from scipy.fftpack import dct

from .base_stat_swfilter import BaseStatSWFilter


class DCTRegressorSWFilter(BaseStatSWFilter):
    """
        Implements 1D Fast Discrete COS transform.
        Only for experiment.
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          first=0,
                          last=None,
                          step=1,
                          **kwargs):
        """

        :param window_seq:
        :param first:
        :param last:
        :param step:
        :param kwargs:
        :return:
        """

        for window in window_seq:
            wlen = len(window)
            if last is None:
                last = wlen
            spec_slice = slice(first, last, step)
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
