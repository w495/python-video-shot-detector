# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_swfilter import BaseSWFilter


class PackSWFilter(BaseSWFilter):
    """
        TODO:
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self, window_seq, func=None, **kwargs):
        """
        
        :param window_seq: 
        :param func: 
        :param kwargs: 
        :return: 
        """
        seq_seq = tuple(
            self.aggregate_windows_gen(window_seq, **kwargs))
        for seq in seq_seq:
            yield sum(seq)

    def aggregate_windows_gen(self, window_seq, **kwargs):
        """
        
        :param window_seq: 
        :param kwargs: 
        :return: 
        """
        for window_features in window_seq:
            yield self.aggregate_window_item(window_features, **kwargs)

    def aggregate_window_item(self, sequence, to_filter=0, **_):
        """
        
        :param sequence: 
        :param to_filter: 
        :param _: 
        :return: 
        """
        if to_filter:
            return self.seq_to_filter(sequence)
        return tuple(sequence)
