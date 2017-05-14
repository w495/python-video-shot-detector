# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import operator

from shot_detector.filters.dsl import (
    DslPlainFilter,
    FilterOperator,
    FilterTuple,

)
from .bulk_filter import BulkFilter


class ForkFilter11(FilterTuple):
    pass


class ForkFilter(DslPlainFilter):
    """
        Slice filter.
    """

    __logger = logging.getLogger(__name__)

    def apply_sequence(self, others):
        """
        
        :param others: 
        :return: 
        """

        filters = list(self.cast_to_apply_sequence(others))
        filters = list(self.cast_to_apply_fork(filters))
        filter_sequence = self.apply_filter_sequence(filters)
        return filter_sequence

    def cast_to_apply_fork(self, filters):
        yield self
        for filter in filters:
            if isinstance(filter, FilterOperator):
                kwargs = vars(filter)
                filter = BulkFilter(**kwargs)
            yield filter

    @staticmethod
    def bulk(op_func, filters=None, *args):
        if filters is None:
            filters = list()
        filters = list(filters)
        filters += args

        filter = BulkFilter(
            op_func=op_func,
            parallel_filters=filters
        )
        return filter

    @classmethod
    def sum(cls, filters=None, *args):
        filter = cls.bulk(operator.add, filters, *args)
        return filter

    @classmethod
    def min(cls, filters=None, *args):
        filter = cls.bulk(min, filters, *args)
        return filter

    @classmethod
    def max(cls, filters=None, *args):
        filter = cls.bulk(max, filters, *args)
        return filter

    @classmethod
    def sub(cls, filters=None, *args):
        filter = cls.bulk(operator.sub, filters, *args)
        return filter
