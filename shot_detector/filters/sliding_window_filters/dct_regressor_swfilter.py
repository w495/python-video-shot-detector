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
            win_len = len(window)
            if last is None:
                last = win_len
            spec_slice = slice(first, last, step)
            # noinspection PyArgumentEqualDefault
            spectrum = dct(window, type=2)
            spectrum = spectrum[spec_slice]
            for win_index, win_item in enumerate(window):
                s_chain = self.spectrum_chain(spectrum,
                                              win_index,
                                              win_len)
                regression_item = 2 * sum(s_chain)
                yield regression_item

    def spectrum_chain(self, spectrum, win_index, win_len):
        for spec_index, spec_item in enumerate(spectrum):
            norm = self.__norm(spec_index, win_len)
            coef_up = math.pi * (2 * win_index - 1) * spec_index
            coef_down = (2 * win_len)
            coef = coef_up / coef_down
            cos_coef = np.cos(coef)
            result = norm * spec_item * cos_coef
            yield result

    @staticmethod
    def __norm(p, win_len):
        x = 2 if 0 == p else 1
        return 1 / (2 * x * win_len)
