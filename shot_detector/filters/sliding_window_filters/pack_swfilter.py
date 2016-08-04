# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_swfilter import BaseSWFilter


class PackSWFilter(BaseSWFilter):
    """
        TODO:
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self, window_seq, func=None, **kwargs):
        seq_seq = tuple(
            self.aggregate_windows_gen(window_seq, **kwargs))

        print('seq_seq[0] = ', len(seq_seq[0]))
        print('seq_seq = ', len(seq_seq))

        print('seq_seq = ', seq_seq[0:3])

        for seq in seq_seq:
            yield sum(seq)

    def aggregate_windows_gen(self, window_seq, **kwargs):
        for window_features in window_seq:
            yield self.aggregate_window_item(window_features, **kwargs)

    def aggregate_window_item(self, sequence, to_filter=0, **_):
        if to_filter:
            return self.seq_to_filter(sequence)
        return tuple(sequence)
