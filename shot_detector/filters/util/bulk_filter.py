# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters.dsl import FilterOperator
from shot_detector.utils.multiprocessing import FuncSeqMapper


class BulkFilter(FilterOperator):
    __logger = logging.getLogger(__name__)

    def map_seq(self, obj_seq, filter_seq, **kwargs):
        """
            Apply filter parallel_filters in independent way.

            Each filter does not affect others.
            It raises RuntimeError(maximum recursion depth exceeded).
            It happens because it calls inside of `filter_objects`
            and it calls `filter_objects` too.
            To escape it use `sys.setrecursionlimit(CONSTANT)`
            where `CONSTANT` is greater than `1000`.

            :raises RuntimeError: maximum recursion depth exceeded.
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

        func_seq_mapper = FuncSeqMapper(
            caller=self
        )

        func_seq = list(
            filter_item.filter_objects_as_list
            for filter_item in filter_seq
        )

        result = func_seq_mapper.map(
            func_seq,
            list(obj_seq),
            **kwargs
        )
        return result
