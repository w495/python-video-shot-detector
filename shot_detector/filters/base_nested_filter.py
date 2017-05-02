# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import itertools
import logging
import sys

import six
from typing import Iterable

# PY2 & PY3 — compatibility
from builtins import zip

if six.PY2:
    # WARNING: only for Python 2
    import pymp
    import pymp.shared

    pymp.config.nested = True

if six.PY3:
    # WARNING: only for Python 3
    pass

from shot_detector.utils.log_meta import should_be_overloaded
from .base_filter import BaseFilter


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
        mapped_seq = self.map_seq(obj_seq, filter_seq, **kwargs)
        reduced_seq = self.reduce_seq(mapped_seq, **kwargs)
        return reduced_seq

    def map_seq(self, obj_seq, filter_seq, use_pymp=False, **kwargs):
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

        #
        # obj_list = list(obj_seq)
        # filter_list =  list(filter_seq)
        #
        # def apply_sfilter(sfilter):
        #     res = sfilter.filter_objects(obj_list, **kwargs)
        #     return list(res)
        #
        #
        #
        # with ProcessPoolExecutor() as executor:
        #      result = executor.map(
        #          apply_sfilter,
        #          filter_list
        #      )
        #
        # return result

        if use_pymp and six.PY2:
            return self._map_parallel_pymp(
                obj_seq,
                filter_seq,
                **kwargs
            )

        else:
            return self._map_sequentially(
                obj_seq,
                filter_seq,
                **kwargs)

    @staticmethod
    def _map_parallel_pymp(obj_seq, filter_seq, **kwargs):
        """
        Applies several filters from filter_seq
        to video frames from obj_seq in parallel manner
        using pymp (OpenMP for Python).

        Under construction

        :param Iterable obj_seq: a sequence of video frames.
        :param Iterable filter_seq: a sequence of filters.
        :param dict kwargs: filter options
        :return:
        """

        # Serialize sequences to plain lists.
        # Pymp cannot work with `sequences`.
        filter_list = list(filter_seq)
        obj_list = list(obj_seq)

        # number of filters in the sequence.
        filter_number = len(filter_list)

        # number of processes (CPUs).
        PROCESS_NUMBER = 64

        # Initialize shared variable
        # that contains data from each process.
        shared_res_dict = pymp.shared.dict(
            {i: {} for i in range(filter_number)}
        )

        with pymp.Parallel(PROCESS_NUMBER, if_=True) as map_proc:
            # In critical section.
            for map_index in map_proc.range(PROCESS_NUMBER):
                # If PROCESS_NUMBER is `greater` than `filter_number`
                # we can use several processes with the same filter,
                # but with different chunks of frame sequence.
                # Use residue sharding schema.
                # So we split obj_list into several chunks
                # or partitions. And handle each partition
                # in dedicated process.

                # Index of current filter.
                filter_index = map_index % filter_number

                # Index of current chunk due to sharding schema.
                chunk_index = map_index // filter_number

                # The total number of chunks due to sharding schema.
                chunk_number = (PROCESS_NUMBER // filter_number)

                # Size of each partition of obj_list.
                chunk_size = len(obj_list) // chunk_number

                chunk_begin = chunk_size * chunk_index
                chunk_end = chunk_size * (chunk_index + 1)

                # map_proc.print(
                #     "{tid}: "
                #     "map_index = {map_index}; "
                #     "filter_index = {filter_index}; "
                #     "lfs = {lfs}; "
                #     "chunk_index = {chunk_index}; "
                #     "chunk_size = {chunk_size}; "
                #     "chunk_number = {chunk_number}; "
                #     "[*] chunk_begin = {chunk_begin}; "
                #     "[*] chunk_end = {chunk_end}; "
                #     "lol = {lol};".format(
                #         tid=map_proc.thread_num,
                #         map_index=map_index,
                #         filter_index=filter_index,
                #         lfs=filter_number,
                #         chunk_index=chunk_index,
                #         chunk_number=chunk_number,
                #         chunk_size=chunk_size,
                #         chunk_begin=chunk_begin,
                #         chunk_end=chunk_end,
                #         lol=len(obj_list)
                #     )
                # )

                # Gets the local filter for this process.
                filter = filter_list[filter_index]

                # Gets the local list of object.
                obj_chunk = obj_list[chunk_begin:chunk_end]

                # Apply the local filter to the chunk.
                local_result_seq = filter.filter_objects(
                    obj_chunk,
                    **kwargs
                )
                local_result_list = list(local_result_seq)
                with map_proc.lock:
                    # Strore local result into shared variable.
                    shared_res_dict[map_index] = local_result_list
                    # Out of critical section.

        # Remap result of partitioned computation.
        # Join local result for each filter.
        final_result_dict = {}
        for map_index, value in shared_res_dict.items():
            filter_index = map_index % filter_number
            chunk_index = map_index // filter_number
            # print(
            #     'map_index = ', map_index,
            #     'filter_index = ', filter_index,
            #     'chunk_index = ', chunk_index)

            final_result_dict.setdefault(filter_index, []).extend(value)

        for filter_index, value in six.iteritems(final_result_dict):
            print('filter_index = ', filter_index, id(shared_res_dict))
            yield value

    @staticmethod
    def _map_sequentially(obj_seq, filter_seq, **kwargs):
        obj_seq_tuple = itertools.tee(obj_seq, len(filter_seq))
        for sfilter, obj_seq in zip(filter_seq, obj_seq_tuple):
            yield sfilter.filter_objects(obj_seq, **kwargs)

    def reduce_seq(self, mapped_seq, **kwargs):
        first_seq, second_seq = tuple(mapped_seq)
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
