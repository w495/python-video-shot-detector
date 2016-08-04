# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class MinStdRegressionSWFilter(BaseStatSWFilter):
    __logger = logging.getLogger(__name__)

    class Atom(object):

        def __init__(self, index, value, state):
            self.index = index
            self.value = value
            # self.state = state

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):

        for window in window_seq:
            x_window = self.split(window, depth=depth, **kwargs)
            for index, item in enumerate(x_window):
                yield item

    def split(self, sequence, **kwargs):
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
                lower_split + upper_split,
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

    def filter_part(self,
                    function_or_none,
                    sequence,
                    replacer=None,
                    **kwargs):
        part = filter(function_or_none, sequence)
        if not part:
            return part
        part_split = self.split_rec(part, **kwargs)
        return part_split

    def extract_values(self, sequence, **kwargs):
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
        values = list(self.extract_values(sequence))
        mean = self.get_mean(list(values), **kwargs)
        return mean
