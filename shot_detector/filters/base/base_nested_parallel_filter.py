# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import collections
import itertools
import logging
# PY2 & PY3 — compatibility
from builtins import zip

from shot_detector.utils.log_meta import should_be_overloaded
from .base_nested_filter import BaseNestedFilter


class BaseNestedParallelFilter(BaseNestedFilter):
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

    parallel_filters = None

    def filter_objects(self, obj_seq, parallel_filters=None, **kwargs):
        if parallel_filters is None:
            parallel_filters = list()

        assert isinstance(obj_seq, collections.Iterable)

        mapped_seq = self.map_seq(obj_seq, parallel_filters, **kwargs)
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
                sequence of filters to apply
            :param bool use_pymp: Py MP flag
            :param dict kwargs:
                optional arguments for passing to another functions
            :return:
        """

        obj_seq_tuple = itertools.tee(obj_seq, len(filter_seq))
        for sfilter, obj_seq in zip(filter_seq, obj_seq_tuple):
            yield sfilter.filter_objects(obj_seq, **kwargs)

    def reduce_seq(self, mapped_seq, **kwargs):
        """
        
        :param mapped_seq: 
        :param kwargs: 
        :return: 
        """

        mapped_tuple = tuple(mapped_seq)
        for item_tuple in zip(*mapped_tuple):
            yield self.reduce_objects_parallel(item_tuple, **kwargs)

    def reduce_objects_parallel(self, item_tuple, **kwargs):
        """
        
        :param tuple item_tuple: 
        :param kwargs: 
        :return: 
        """

        first = item_tuple[0]

        feature_seq = self.object_features(item_tuple, **kwargs)

        reduced_feature = self.reduce_features_parallel(
            feature_seq,
            **kwargs
        )
        return self.update_object(
            obj=first,
            feature=reduced_feature,
            **kwargs
        )

    @should_be_overloaded
    def reduce_features_parallel(self, feature_seq, **kwargs):
        """
        
        :param first: 
        :param _: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        return tuple(feature_seq)
