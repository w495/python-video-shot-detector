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

    def filter_features(self, feature_iterable, **kwargs):
        assert isinstance(feature_iterable, collections.Iterable)

        if self.sequential_filters:
            filtered_iterable = self.apply_sequentially(
                feature_iterable=feature_iterable,
                filter_iterable=self.sequential_filters,
                **kwargs
            )
            return filtered_iterable
        if self.parallel_filters:
            filtered_iterable = self.apply_parallel(
                feature_iterable=feature_iterable,
                filter_iterable=self.parallel_filters,
                **kwargs
            )
            return filtered_iterable
        return super(BaseNestedFilter, self).filter_features(feature_iterable, **kwargs)

    def apply_parallel(self, feature_iterable, filter_iterable, **kwargs):
        a_, b_ = tuple(self.map_parallel(feature_iterable, filter_iterable, **kwargs))

        reduced_iterable = self.reduce_parallel__(a_, b_)

        return reduced_iterable

    def reduce_parallel__(self, a_, b_):

        # print ('a_ = ', a_, b_)

        for x, y in itertools.izip_longest(a_, b_):
            yield self.reduce_parallel(x, y)

            #
            # return a_
            #
            #     # print ('feature_tuple@ =', x, y)
            #     # yield x-y

    def reduce_parallel(self, *args):
        self.__logger.debug('filter_feature_item: not implemented')
        return args[0]

    @staticmethod
    def map_parallel(feature_iterable, filter_iterable, **kwargs):
        feature_iterable_tuple = itertools.tee(feature_iterable, len(filter_iterable))
        for sfilter, feature_iterable in itertools.izip(filter_iterable, feature_iterable_tuple):
            print('sfilter = ', sfilter)
            yield sfilter.filter_features(feature_iterable, **kwargs)

    # noinspection PyUnusedLocal
    @staticmethod
    def apply_sequentially(feature_iterable, filter_iterable, **_kwargs):

        for subfilter in filter_iterable:
            feature_iterable = subfilter.filter_features(feature_iterable)

        return feature_iterable
