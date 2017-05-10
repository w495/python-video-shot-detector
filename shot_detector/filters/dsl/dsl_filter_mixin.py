# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import collections
import logging

from shot_detector.utils.dsl import BaseDslOperatorMixin
from shot_detector.utils.dsl.dsl_kwargs import dsl_kwargs_decorator

class DslFilterMixin(BaseDslOperatorMixin):
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
        return self.sequential(other)

    def __ror__(self, other):
        """
        :param Filter other:
        :return:
        """

        return self.sequential(other)

    def sequential(self, other):
        """

        :param other:
        :return:
        """
        from .filter_cast_features import FilterCastFeatures
        from .filter_sequence import FilterSequence

        if not isinstance(other, DslFilterMixin):
            other = FilterCastFeatures(
                cast=other,
            )
        return FilterSequence(
            sequential_filters=[
                self, other
            ],
        )

    def apply_operator(self,
                       op_func=None,
                       others=None,
                       mode=None,
                       **kwargs):
        """

        :param other: 
        :param op: 
        :param is_right: 
        :return: 
        """

        from .filter_operator import FilterOperator as Fo

        other = others[0]

        if not isinstance(other, DslFilterMixin):
            other = self.scalar_to_filter(
                value=other,
            )

        mode = Fo.LEFT
        if mode is self.OPERATOR_RIGHT:
            mode = Fo.RIGHT

        return Fo(
            parallel_filters=[self, other],
            op_func=op_func,
            mode=mode,
            **kwargs
        )

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
