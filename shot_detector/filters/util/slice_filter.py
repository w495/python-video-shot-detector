# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import itertools
import logging

from shot_detector.filters.dsl import DslPlainFilter


class SliceFilter(DslPlainFilter):
    """
        Slice filter.
    """

    __logger = logging.getLogger(__name__)

    def filter_objects(self,
                       sequence,
                       start=0,
                       stop=None,
                       step=None,
                       **kwargs):
        """

        :param sequence:
        :param start:
        :param stop:
        :param step:
        :param kwargs:
        :return:
        """

        i_seq = iter(sequence)
        sliced_sequence = itertools.islice(
            i_seq,
            start=start,
            stop=start,
            step=step,
        )

        return sliced_sequence
