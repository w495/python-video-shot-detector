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
)
from .bulk_filter import BulkFilter


class ForkFilter(DslPlainFilter):
    """
        Slice filter_item.
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
        """
        
        :param filters: 
        :return: 
        """
        yield self
        for filter_item in filters:
            if isinstance(filter_item, FilterOperator):
                kwargs = vars(filter_item)
                filter_item = BulkFilter(**kwargs)
            yield filter_item

    @staticmethod
    def bulk(op_func, filters=None, *args):
        """
        
        :param op_func: 
        :param filters: 
        :param args: 
        :return: 
        """
        if filters is None:
            filters = list()
        filters = list(filters)
        filters += args

        bulk_filter = BulkFilter(
            op_func=op_func,
            parallel_filters=filters
        )
        return bulk_filter

    @classmethod
    def sum(cls, filters=None, *args):
        """
        
        :param filters: 
        :param args: 
        :return: 
        """
        bulk_filter = cls.bulk(operator.add, filters, *args)
        return bulk_filter

    @classmethod
    def min(cls, filters=None, *args):
        """
        
        :param filters: 
        :param args: 
        :return: 
        """
        bulk_filter = cls.bulk(min, filters, *args)
        return bulk_filter

    @classmethod
    def max(cls, filters=None, *args):
        """
        
        :param filters: 
        :param args: 
        :return: 
        """
        bulk_filter = cls.bulk(max, filters, *args)
        return bulk_filter

    @classmethod
    def sub(cls, filters=None, *args):
        """
        
        :param filters: 
        :param args: 
        :return: 
        """
        bulk_filter = cls.bulk(operator.sub, filters, *args)
        return bulk_filter
