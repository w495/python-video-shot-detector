# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import itertools

from .base_stat_swfilter import BaseStatSWFilter


class MinStdRegressionSWFilter(BaseStatSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    class Atom(object):
        """
            ...
        """

        def __init__(self, index, value, state):
            self.index = index
            self.value = value
            self.state = state

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

    def split(self, sequence, **kwargs):
        """
        
        :param sequence: 
        :param kwargs: 
        :return: 
        """
        indexed_window = list(
            self.Atom(
                index=index,
                value=value,
                state=False
            )
            for index, value in enumerate(sequence)
        )
        indexed_window = self.split_rec(indexed_window, **kwargs)
        values = list(self.extract_values(indexed_window))
        return values

    def split_rec(self, sequence, depth=0, **kwargs):
        """
        
        :param sequence: 
        :param depth: 
        :param kwargs: 
        :return: 
        """
        pivot = self.pivot(sequence, **kwargs)
        if depth > 0:
            upper_split = self.filter_part(
                lambda item:
                item.value > pivot,
                sequence,
                depth=depth - 1,
                replacer=pivot,
                **kwargs
            )
            lower_split = self.filter_part(
                lambda item:
                item.value <= pivot,
                sequence,
                depth=depth - 1,
                replacer=pivot,
                **kwargs
            )
            sequence = sorted(
                itertools.chain(lower_split, upper_split),
                key=lambda item:
                item.index
            )
        else:
            sequence = list(
                self.replace_items(
                    sequence,
                    replacer=pivot,
                    **kwargs
                )
            )
        return sequence

    # noinspection PyUnusedLocal
    def filter_part(self,
                    function_or_none,
                    sequence,
                    replacer=None,
                    **kwargs):
        """
        
        :param function_or_none: 
        :param sequence: 
        :param replacer: 
        :param kwargs: 
        :return: 
        """
        part = filter(function_or_none, sequence)
        if not part:
            return part
        part_split = self.split_rec(part, **kwargs)
        return part_split

    @staticmethod
    def extract_values(sequence, **_):
        """
        
        :param sequence: 
        :param _: 
        :return: 
        """
        for item in sequence:
            yield item.value

    def replace_items(self, sequence, replacer=None, **kwargs):
        """

        (Works only in leafs)
        :param sequence:
        :param replacer:
        :param kwargs:
        :return:
        """
        for index, item in enumerate(sequence):
            yield self.Atom(
                index=item.index,
                value=replacer,
                state=True
            )

    def pivot(self, sequence, **kwargs):
        """
        
        :param sequence: 
        :param kwargs: 
        :return: 
        """
        values = list(self.extract_values(sequence))
        mean = self.get_mean(list(values), **kwargs)
        return mean
