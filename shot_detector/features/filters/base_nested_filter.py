# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import itertools
import logging

from .base_filter import BaseFilter

class BaseNestedFilter(BaseFilter):
    __logger = logging.getLogger(__name__)

    sequential_filters = None
    parallel_filters = None

    def __init__(self, sequential_filters=None, parallel_filters=None, **kwargs):
        if sequential_filters:
            self.sequential_filters = sequential_filters
        if parallel_filters:
            self.parallel_filters = parallel_filters

        super(BaseNestedFilter, self).__init__(**kwargs)

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
        return super(BaseNestedFilter, self).filter_objects(obj_seq, **kwargs)

    def apply_parallel(self, obj_seq, filter_seq, **kwargs):
        a_, b_ = tuple(self.map_parallel(obj_seq, filter_seq, **kwargs))

        reduced_seq = self.reduce_parallel__(a_, b_, **kwargs)

        return reduced_seq

    def reduce_parallel__(self, a_, b_, **kwargs):
        for first, second in itertools.izip_longest(a_, b_):
            yield self.reduce_objects_parallel(first, second, **kwargs)

    def reduce_objects_parallel(self, first, second, *args, **kwargs):
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


    def reduce_features_parallel(self, first, _, *args, **kwargs):
        self.__logger.debug('filter_feature_item: not implemented')
        return first

    @staticmethod
    def map_parallel(obj_seq, filter_seq, **kwargs):
        obj_seq_tuple = itertools.tee(obj_seq, len(filter_seq))
        for sfilter, obj_seq in itertools.izip(filter_seq, obj_seq_tuple):
            yield sfilter.filter_objects(obj_seq, **kwargs)

    # noinspection PyUnusedLocal
    @staticmethod
    def apply_sequentially(obj_seq, filter_seq, **_kwargs):

        for subfilter in filter_seq:
            obj_seq = subfilter.filter_objects(obj_seq)

        return obj_seq
