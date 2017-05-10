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
from concurrent.futures import ProcessPoolExecutor

from shot_detector.filters.dsl import DslNestedParallelFilter


class BulkFilter(DslNestedParallelFilter):
    __logger = logging.getLogger(__name__)

    def __init__(self,
                 reducer=None,
                 **kwargs):
        self.reducer = reducer
        super(BulkFilter, self).__init__(**kwargs)

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
            :param bool use_pymp: Py MP flag
            :param dict kwargs:
                optional arguments for passing to another functions
            :return:
        """

        futures = self.future_list(obj_seq, filter_seq, **kwargs)
        result = self.joined_map_seq(futures)
        return result

    def future_list(self, obj_seq, filter_seq, **kwargs):
        futures = self.future_seq(obj_seq, filter_seq, **kwargs)
        futures = list(futures)  # !important
        return futures

    def future_seq(self, obj_seq, filter_seq, **kwargs):
        obj_list = list(obj_seq)
        with ProcessPoolExecutor() as executor:
            for filter in filter_seq:
                future = executor.submit(
                    filter.filter_objects_as_list,
                    obj_list,
                    **kwargs
                )
                yield future

    @staticmethod
    def joined_map_seq(futures):
        for future in futures:
            res = future.result()
            yield res

    def reduce_features_parallel(self, args, **kwargs):
        """

        :param args: 
        :param kwargs: 
        :return: 
        """

        reduced = self.reducer(args)
        return reduced
