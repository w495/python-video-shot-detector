# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import collections
import itertools
import logging

from shot_detector.utils.dsl import DslOperatorMixin
from shot_detector.utils.dsl.dsl_kwargs import dsl_kwargs_decorator


class DslFilterMixin(DslOperatorMixin):
    """
        Basic filter mixin to build Filter-DSL
    """
    __logger = logging.getLogger(__name__)

    @staticmethod
    def dsl_kwargs_decorator(*dsl_rules):
        """
        
        :param dsl_rules: 
        :return: 
        """
        return dsl_kwargs_decorator(*dsl_rules)

    def __or__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_sequence([other])

    def __ror__(self, other):
        """
        :param Filter other:
        :return:
        """

        return self.apply_sequence([other])

    def apply_sequence(self, others):
        """

        :param other:
        :return:
        """

        filters = self.cast_to_apply_sequence(others)
        filter_sequence = self.apply_filter_sequence(filters)
        return filter_sequence

    def apply_filter_sequence(self, filters):
        """
        
        Extends current own `sequential_filters` with `filters`
        or creates a new `FilterSequence`.
        
        :param filters: 
        :return:
        """
        from .filter_sequence import FilterSequence

        if isinstance(self, FilterSequence):
            self_filters = self.sequential_filters
            joined_filters = itertools.chain(self_filters, filters)
            filter_sequence = self
        else:
            joined_filters = itertools.chain([self], filters)
            filter_sequence = FilterSequence
        joined_filter_list = list(joined_filters)
        filter_sequence = filter_sequence(
            sequential_filters=joined_filter_list
        )

        return filter_sequence

    #@staticmethod
    def cast_to_apply_sequence(self, others):
        """
        
        :param others: 
        :return: 
        """
        from .filter_cast_features import FilterCastFeatures

        for other in others:
            if isinstance(other, tuple):
                other = DslFilterMixin.tuple(*other)
            if not isinstance(other, DslFilterMixin):
                other = FilterCastFeatures(
                    op_func=other,
                    parallel_filters=[self]
                )

            yield other

    def apply_operator(self,
                       op_func=None,
                       others=None,
                       op_mode=None,
                       **kwargs):
        """
        
        :param op_func: 
        :param others: 
        :param op_mode: 
        :param kwargs: 
        :return: 
        """
        filters = self.cast_to_apply_operator(others)

        filter_operator = self.apply_filter_operator(
            op_func=op_func,
            filters=filters,
            op_mode=op_mode,
        )

        return filter_operator

    def apply_filter_operator(self,
                              op_func=None,
                              filters=None,
                              op_mode=None,
                              **kwargs):
        """
        
        :param op_func: 
        :param filters: 
        :param op_mode: 
        :param kwargs: 
        :return: 
        """

        from .filter_operator import FilterOperator, FilterOperatorMode

        fo_op_mode = FilterOperatorMode.LEFT
        if op_mode is self.Operaror.RIGHT:
            fo_op_mode = FilterOperatorMode.RIGHT

        # joined_filters = itertools.chain([self], filters)

        filter_operator = FilterOperator(
            op_func=op_func,
            op_mode=fo_op_mode,
            # parallel_filters=list(joined_filters),
            **kwargs
        )

        if isinstance(self, FilterOperator) and filter_operator == self:
            self_filters = self.parallel_filters
            joined_filters = itertools.chain(self_filters, filters)
            filter_operator = self
        else:
            joined_filters = itertools.chain([self], filters)

        joined_filter_list = list(joined_filters)
        filter_operator = filter_operator(
            parallel_filters=joined_filter_list
        )

        return filter_operator

    @classmethod
    def tuple(cls, *args):
        """
        :param Filter first:
        :param Filter second:
        :return:
        """
        from .filter_tuple import FilterTuple
        filter_operator = FilterTuple(
            parallel_filters=list(args)
        )
        return filter_operator

    def cast_to_apply_operator(self, others):
        for other in others:
            if not isinstance(other, DslFilterMixin):
                other = self.scalar_to_filter(
                    value=other,
                )
            yield other

    def to_filter(self, value):
        """

        :param value: 
        :return: 
        """
        if isinstance(value, collections.Iterable):
            return self.seq_to_filter(value)
        return self.scalar_to_filter(value)

    @staticmethod
    def seq_to_filter(value):
        """

        :param value: 
        :return: 
        """
        from .filter_cast_seq_value import FilterCastSeqValue
        return FilterCastSeqValue(seq=value)

    @staticmethod
    def scalar_to_filter(value):
        """

        :param value: 
        :return: 
        """
        from .filter_cast_scalar_value import FilterCastScalarValue
        return FilterCastScalarValue(value=value)

    def __contains__(self, item):
        """
        :param Filter item:
        :return:
        """
        return self.intersect(item)

    def i(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return self.intersect(*args, **kwargs)

    def intersect(self, other, threshold=0):
        """

        :param other:
        :param threshold:
        :return:
        """
        from .filter_intersection import FilterIntersection

        return FilterIntersection(
            parallel_filters=[self, other],
            threshold=threshold
        )
