# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from .min_std_regression_swfilter import MinStdRegressionSWFilter


class NikitinSWFilter(MinStdRegressionSWFilter):
    """
        Need to be calibrated
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):

        for window in window_seq:
            x_window = self.split(window, depth=depth, **kwargs)
            for index, item in enumerate(x_window):
                yield item

    def split(self, sequence, use_first=True, **kwargs):
        indexed_window = list(
            self.Atom(
                index=index,
                value=value,
                state=0
            )
            for index, value in enumerate(sequence)
        )
        indexed_window = self.split_rec(indexed_window, **kwargs)

        indexed_window += [indexed_window[-1]]

        for prev, curr in zip(indexed_window[:-1], indexed_window[1:]):

            number = len(prev.state) if use_first else len(curr.state)

            seq = np.linspace(
                prev.value,
                curr.value,
                num=number
            )

            for item in seq:
                yield item

    def replace_items(self,
                      sequence,
                      replacer=None,
                      use_first=True,
                      **kwargs):

        for index, item in enumerate(sequence):
            if use_first and (index == 0):
                yield self.Atom(
                    index=item.index,
                    value=replacer,
                    state=sequence
                )
            elif (index == len(sequence) - 1):
                yield self.Atom(
                    index=item.index,
                    value=replacer,
                    state=sequence
                )

                # def centre_both(self,
                #                 objects,
                #                 features,
                #                 strict_windows=False,
                #                 **kwargs):
                #     """
                #
                #     :param objects:
                #     :param features:
                #     :param strict_windows:
                #     :param kwargs:
                #     :return:
                #     """
                #
                #     features = self.centre_window(features, **kwargs)
                #     return objects, features
                #
                # def centre_window(self, window, window_size=0, **_):
                #     """
                #
                #     :param window:
                #     :param window_size:
                #     :param _:
                #     :return:
                #     """
                #     window = itertools.islice(
                #         window,
                #         window_size,
                #         None,
                #     )
                #     return window
