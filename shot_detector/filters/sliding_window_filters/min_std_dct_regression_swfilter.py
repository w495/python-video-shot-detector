# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import math

import numpy as np
from scipy.fftpack import dct

from .min_std_regression_swfilter import MinStdRegressionSWFilter


class MinStdDCTRegressionSWFilter(MinStdRegressionSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):
        """
        
        :param window_seq: 
        :param depth: 
        :param kwargs: 
        :return: 
        """

        for window in window_seq:
            x_window = self.split(window, depth=depth, **kwargs)
            for index, item in enumerate(x_window):
                yield item

                # if index == 0:
                #     yield -0.1
                # else:
                #     yield item

    def replace_items(self, sequence, replacer=None, **kwargs):
        """
        
        :param sequence: 
        :param replacer: 
        :param kwargs: 
        :return: 
        """
        values = list(self.extract_values(sequence))

        values = list(self.dct_window(values))

        for index, item in enumerate(sequence):
            if not item.state:
                yield self.Atom(
                    index=item.index,
                    value=values[index],
                    state=True
                )
            else:
                yield item

    def dct_window(self,
                   window,
                   first=0,
                   last=None,
                   step=1,
                   **_):
        """
        
        :param window: 
        :param first: 
        :param last: 
        :param step: 
        :param _: 
        :return: 
        """
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
        """
        
        :param spectrum: 
        :param win_index: 
        :param win_len: 
        :return: 
        """
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
        """
        
        :param p: 
        :param win_len: 
        :return: 
        """
        x = 2 if 0 == p else 1
        return 1 / (2 * x * win_len)
