# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import collections
import logging

from .base_nested_filter import BaseNestedFilter


class BaseNestedSequentialFilter(BaseNestedFilter):
    """
        Apply `sequential_filters` or `parallel_filters` inside itself.

        It raises RuntimeError(maximum recursion depth exceeded).
        It happens because `filter_objects` can be called inside
        other `filter_objects` of another objects of the same class.
        To escape it use `sys.setrecursionlimit(CONSTANT)`
        where `CONSTANT` is greater than `1000`.
        Beware that some operating systems may start running into
        problems if you go much higher due to limited stack space.

        :raises RuntimeError: maximum recursion depth exceeded.
            It happens because `filter_objects` can be called inside
            other  `filter_objects` of another objects of the same
            class
    """
    __logger = logging.getLogger(__name__)

    def filter_objects(self, obj_seq, sequential_filters=None,
                       **kwargs):
        """
            Apply filter sequential_filters consecutively.

            Each filter output is input for the next filter.
            It raises RuntimeError(maximum recursion depth exceeded).
            It happens because it calls inside of `filter_objects`
            and it calls `filter_objects` too.
            To escape it use `sys.setrecursionlimit(CONSTANT)`
            where `CONSTANT` is greater than `1000`.

            :raises RuntimeError: maximum recursion depth exceeded:
                It happens because it calls inside of
                `filter_objects` and it calls
                `filter_objects` too.
            :param collections.Iterable obj_seq:
                sequence of objects to filter
            :param collections.Sequence filter_seq:
                sequence of filters to apply
            :param dict kwargs:
                optional arguments for passing to another functions
            :return:

        """

        if sequential_filters is None:
            sequential_filters = list()
        assert isinstance(obj_seq, collections.Iterable)
        for sub_filter in sequential_filters:
            obj_seq = sub_filter.filter_objects(obj_seq, **kwargs)
        return obj_seq
