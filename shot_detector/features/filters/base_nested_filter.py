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
            filtered_iterable= self.apply_parallel(
                feature_iterable=feature_iterable,
                filter_iterable=self.parallel_filters,
                **kwargs
            )
            return filtered_iterable
        return feature_iterable

    def apply_parallel(self, feature_iterable, filter_iterable, **kwargs):
        feature_iterables = self.map_parallel(feature_iterable, filter_iterable, **kwargs)
        reduced_iterable = itertools.imap(self.reduce_parallel, *feature_iterables)
        return reduced_iterable

    def reduce_parallel(self, *args):
        self.__logger.debug('filter_feature_item: not implemented')
        return args[0]

    @staticmethod
    def map_parallel(feature_iterable, filter_iterable, **kwargs):
        for subfilter in filter_iterable:
            yield subfilter.filter_features(feature_iterable)

    @staticmethod
    def apply_sequentially(feature_iterable, filter_iterable, **kwargs):
        for subfilter in filter_iterable:
            feature_iterable = subfilter.filter_features(feature_iterable)
        return feature_iterable
