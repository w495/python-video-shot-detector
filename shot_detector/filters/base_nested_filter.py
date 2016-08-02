# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import itertools
import logging
import sys


# PY2 & PY3 — compatibility
from builtins import zip

# import pymp
# import pymp.shared

from shot_detector.utils.log_meta import should_be_overloaded
from .base_filter import BaseFilter

# pymp.config.nested = True


class BaseNestedFilter(BaseFilter):
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

    sequential_filters = None
    parallel_filters = None
    use_pymp = False

    def __init__(self,
                 sequential_filters=None,
                 parallel_filters=None,
                 use_pymp=False,
                 recursion_limit=None,
                 **kwargs):
        if sequential_filters:
            self.sequential_filters = sequential_filters
        if parallel_filters:
            self.parallel_filters = parallel_filters

        if use_pymp is not None:
            self.use_pymp = use_pymp

        if recursion_limit:
            original_recursion_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(recursion_limit)
            self.__logger.warn(
                "recursion limit was changed "
                "from {} to {}".format(
                    original_recursion_limit,
                    recursion_limit
                )
            )

        super(BaseNestedFilter, self).__init__(
            sequential_filters=self.sequential_filters,
            parallel_filters=self.parallel_filters,
            **kwargs
        )

    #
    # @classmethod
    # def queue_process_pool_getter(cls):
    #     if not cls.__queue_process_pool:
    #         cls.__queue_process_pool = FilterQueueProcessPool()
    #         cls.__queue_process_pool.start()
    #     return cls.__queue_process_pool

    # @property
    # def queue_process_pool(self):
    #     return type(self).queue_process_pool


    def filter_objects(self, obj_seq, **kwargs):
        assert isinstance(obj_seq, collections.Iterable)
        if self.sequential_filters:
            filtered_seq = self.apply_sequentially(
                obj_seq=obj_seq,
                filter_seq=self.sequential_filters,
                **kwargs
            )
            return filtered_seq
        if self.parallel_filters:
            filtered_seq = self.apply_parallel(
                obj_seq=obj_seq,
                filter_seq=self.parallel_filters,
                **kwargs
            )
            return filtered_seq
        return super(BaseNestedFilter, self).filter_objects(obj_seq,
                                                            **kwargs)

    def apply_parallel(self, obj_seq, filter_seq, **kwargs):
        first_seq, second_seq = tuple(
            self.map_parallel(obj_seq, filter_seq, **kwargs)
        )
        reduced_seq = self.zip_objects_parallel(first_seq, second_seq,
                                                **kwargs)
        return reduced_seq

    @staticmethod
    def map_parallel(obj_seq, filter_seq, use_pymp=False, **kwargs):
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
                seruence of filters to apply
            :param dict kwargs:
                optional arguments for passing to another functions
            :return:
        """
        # if use_pymp:
        #
        #     lfs = len(tuple(filter_seq))
        #
        #     res_dict = pymp.shared.dict({i: {} for i in xrange(lfs)})
        #
        #     filter_list = list(filter_seq)
        #     obj_list = list(obj_seq)
        #
        #     OBJ_PROC = lfs
        #
        #     with pymp.Parallel(OBJ_PROC, if_=True) as map_proc:
        #         for map_index in map_proc.range(OBJ_PROC):
        #             filter_index = map_index % lfs
        #             chunk_index = map_index // lfs
        #
        #             chunk_number = (OBJ_PROC // lfs)
        #             chunk_size = len(obj_list) // chunk_number
        #
        #             chunk_begin = chunk_size * chunk_index
        #             chunk_end = chunk_size * (chunk_index + 1)
        #
        #             map_proc.print(
        #                 "{tid}: "
        #                 "map_index = {map_index}; "
        #                 "filter_index = {filter_index}; "
        #                 "lfs = {lfs}; "
        #                 "chunk_index = {chunk_index}; "
        #                 "chunk_size = {chunk_size}; "
        #                 "chunk_number = {chunk_number}; "
        #                 "[*] chunk_begin = {chunk_begin}; "
        #                 "[*] chunk_end = {chunk_end}; "
        #                 "lol = {lol};".format(
        #                     tid=map_proc.thread_num,
        #                     map_index=map_index,
        #                     filter_index=filter_index,
        #                     lfs=lfs,
        #                     chunk_index=chunk_index,
        #                     chunk_number=chunk_number,
        #                     chunk_size=chunk_size,
        #                     chunk_begin=chunk_begin,
        #                     chunk_end=chunk_end,
        #                     lol=len(obj_list)
        #                 )
        #             )
        #
        #             sfilter = filter_list[filter_index]
        #             obj_chunk = obj_list[chunk_begin:chunk_end]
        #             res_chunk_seq = sfilter.filter_objects(
        #                 obj_chunk,
        #                 **kwargs
        #             )
        #             res_chunk_list = list(res_chunk_seq)
        #             with map_proc.lock:
        #                 res_dict[map_index] = res_chunk_list
        #
        #     x_result_dict = {}
        #     for map_index, value in res_dict.items():
        #         filter_index = map_index % lfs
        #         chunk_index = map_index // lfs
        #         print(
        #             'map_index = ', map_index,
        #             'filter_index = ', filter_index,
        #             'chunk_index = ', chunk_index)
        #
        #         x_result_dict.setdefault(filter_index, []).extend(value)
        #
        #     for filter_index, value in six.iteritems(x_result_dict):
        #         print('filter_index = ', filter_index, id(res_dict))
        #         yield value
        #
        # else:

        obj_seq_tuple = itertools.tee(obj_seq,len(filter_seq))
        for sfilter, obj_seq in zip(filter_seq, obj_seq_tuple):
            yield sfilter.filter_objects(obj_seq, **kwargs)


    def zip_objects_parallel(self, first_seq, second_seq, **kwargs):
        for first, second in zip(first_seq, second_seq):
            yield self.reduce_objects_parallel(first, second, **kwargs)

    def reduce_objects_parallel(self, first, second, *args, **kwargs):

        # print ('first.feature',  first.feature,
        #        'second.feature',  second.feature)

        reduced_feature = self.reduce_features_parallel(
            first.feature,
            second.feature,
            *args,
            **kwargs
        )
        return self.update_object(
            obj=first,
            feature=reduced_feature,
            **kwargs
        )

    @should_be_overloaded
    def reduce_features_parallel(self, first, _, *args, **kwargs):
        return first

    # noinspection PyUnusedLocal
    def apply_sequentially(self, obj_seq, filter_seq, **kwargs):
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
                seruence of filters to apply
            :param dict kwargs:
                optional arguments for passing to another functions
            :return:

        """
        for subfilter in filter_seq:
            obj_seq = subfilter.filter_objects(obj_seq, **kwargs)

        return obj_seq


if __name__ == '__main__':
    pass
