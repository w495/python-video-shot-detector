# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import operator

from shot_detector.filters.dsl import DslPlainFilter
from shot_detector.filters.util import BulkFilter


class Filter(DslPlainFilter):
    """
        Basic feature filter
    """
    __logger = logging.getLogger(__name__)

    PARALLEL_MODE_FORK = object()
    PARALLEL_MODE_JOIN = object()

    @staticmethod
    def fork(cls):
        """
        
        :param cls: 
        :return: 
        """
        p_filter = cls(parallel_mode=cls.PARALLEL_MODE_FORK)
        return p_filter

    @staticmethod
    def join(cls):
        """
        
        :param cls: 
        :return: 
        """
        p_filter = cls(parallel_mode=cls.PARALLEL_MODE_JOIN)
        return p_filter

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
        bulk_filter = cls.bulk(sum, filters, *args)
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
