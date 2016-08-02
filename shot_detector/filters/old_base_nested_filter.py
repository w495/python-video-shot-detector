# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import itertools
import logging
import sys

import pymp
import pymp.shared

from shot_detector.utils.log_meta import should_be_overloaded
from .base_filter import BaseFilter
pymp.config.nested = True

from shot_detector.utils.multiprocessing import BaseQueueProcessPool


class FilterQueueProcessPool(BaseQueueProcessPool):

    @staticmethod
    def handle_task(func, *args, **kwargs):
        result = func(*args, **kwargs)
        return list(result)



class BaseNestedFilterGlobals(object):
    def __init__(self, pool = None):
        self.pool = pool


class OldBaseNestedFilter(BaseFilter):
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

    globals = BaseNestedFilterGlobals()



    def __init__(self,
                 sequential_filters=None,
                 parallel_filters=None,
                 recursion_limit=None,
                 **kwargs):
        if sequential_filters:
            self.sequential_filters = sequential_filters
        if parallel_filters:
            self.parallel_filters = parallel_filters

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

        # if not self.globals.pool:
        #     self.globals.pool = FilterQueueProcessPool()

        super(OldBaseNestedFilter, self).__init__(
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
        return super(OldBaseNestedFilter, self).filter_objects(obj_seq, **kwargs)

    def apply_parallel(self, obj_seq, filter_seq, **kwargs):
        self.__logger.error('fix 1')

        first_seq, second_seq = tuple(
            self.map_parallel(obj_seq, filter_seq, **kwargs)
        )
        self.__logger.error('fix 2', )

        reduced_seq = self.zip_objects_parallel(first_seq, second_seq, **kwargs)


        # for i, res in enumerate(reduced_seq):
        #     print (i, 'reduced_seq = ',  res.feature)
        #

        return reduced_seq

    def map_parallel(self, obj_seq, filter_seq, **kwargs):
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


        obj_seq_tuple = itertools.tee(obj_seq,len(filter_seq))


        # #
        # # queue_process_pool = ProcessPool()
        # #
        # #
        # # def apply_filter((sfilter, obj_seq),):
        # #     x = sfilter.filter_objects(obj_seq, **kwargs)
        # #
        # #     return list(x)
        # #
        # # def make_data(sfilter, obj_seq):
        # #     dumped_data = dill.dumps(dict(
        # #         func=sfilter,
        # #         args=obj_seq,
        # #     ))
        # #     return dumped_data
        # #
        # # filter_seq2 = (
        # #     (sfilter, list(obj_seq))
        # #     for sfilter, obj_seq
        # #     in itertools.izip(filter_seq, obj_seq_tuple)
        # # )
        # #
        # # return queue_process_pool.imap(apply_filter, filter_seq2)
        #
        # with self.globals.pool as queue_pool:
        # #with self.queue_process_pool as queue_pool:
        #     for sfilter, obj_seq in itertools.izip(filter_seq, obj_seq_tuple):
        #         queue_pool.put_task(
        #             sfilter.filter_objects,
        #             list(obj_seq),
        #             **kwargs
        #         )
        #
        #
        #     res = queue_pool.join(reduce_func=tuple)
        #     print (len(res[0]))
        # return res

        #
        # def apply_filter(sfilter, obj_seq, kwargs):
        #
        #     print ('    inside apply_filter')
        #
        #     if not kwargs:
        #         kwargs = dict()
        #
        #     x = sfilter.filter_objects(obj_seq, **kwargs)
        #
        #
        #     return list(x)

        # job_list = []
        # for sfilter, obj_seq in itertools.izip(filter_seq, obj_seq_tuple):
        #     print (obj_seq )
        #     job_list += [gen_server.submit(
        #         apply_filter,
        #         args=(sfilter, list(obj_seq), kwargs),
        #         depfuncs=(),
        #         modules=(
        #             'six',
        #             'Filter',
        #             'BaseSWFilter'
        #         ),
        #         globals=globals()
        #     )]
        # self.__logger.warn('job_list starts')


        # for job in job_list:
        #     self.__logger.warn('job_list call start %s', gen_server.job_server.print_stats())
        #     result = job()
        #     self.__logger.warn('job_list call ends %s', job)
        #     yield result
        #     self.__logger.warn('job_list call yields %s', job)

        self.__logger.warn('job_list end')




        # filter_seq, filter_seq_2 = itertools.tee(filter_seq)
        #
        # obj_seq_tuple, obj_seq_tuple_2 = itertools.tee(obj_seq_tuple)



        # lfs = len(tuple(filter_seq))
        #
        # res_list = pymp.shared.list()
        # rlock = pymp.shared.rlock()
        #
        # with pymp.Parallel(lfs, if_= True) as p:
        #     sec_range = p.xrange(lfs)
        #     with rlock:
        #         p_seq = itertools.izip(sec_range, filter_seq, obj_seq_tuple)
        #         for num, sfilter, obj_seq in p_seq:
        #             # p.print(p.num_threads, p.thread_num, sfilter,
        #             #         obj_seq , num)
        #
        #             x = sfilter.filter_objects(list(obj_seq), **kwargs)
        #             y = list(x)
        #             res_list += [y]
        #
        #
        # return res_list


        for sfilter, obj_seq in itertools.izip(filter_seq,
                                               obj_seq_tuple):
            yield sfilter.filter_objects(obj_seq, **kwargs)

    def zip_objects_parallel(self, first_seq, second_seq, **kwargs):
        for first, second in itertools.izip(first_seq, second_seq):
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