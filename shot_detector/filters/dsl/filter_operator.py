# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import operator

import numpy as np

from .dsl_nested_parallel_filter import DslNestedParallelFilter


class FilterOperator(DslNestedParallelFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    BOOLEAN_OPERATORS = (
        operator.lt,
        operator.gt,
        operator.le,
        operator.ge,
        operator.eq,
        operator.ne
    )

    RIGHT = object()
    LEFT = object()

    def __init__(self,
                 op_func=None,
                 mode=None,
                 **kwargs):

        if op_func:
            self.op_func = op_func
        if mode:
            self.mode = mode
        super(FilterOperator, self).__init__(
            **kwargs
        )

    def reduce_features_parallel(self, feature_tuple, **kwargs):
        """
        
        :param first: 
        :param second: 
        :param op_func: 
        :param args: 
        :param kwargs: 
        :return: 
        """

        return self.apply_op_func(
            feature_tuple,
            **kwargs
        )

    def apply_op_func(self, feature_tuple, **kwargs):
        """
        
        :param first: 
        :param second: 
        :param op_func: 
        :param is_right: 
        :param kwargs: 
        :return: 
        """

        feature_tuple = tuple(feature_tuple)

        if self.mode is self.RIGHT:
            feature_tuple = reversed(feature_tuple)

        return self._apply_op_func(
            feature_tuple,
            **kwargs
        )

    def _apply_op_func(self, feature_tuple, **_):
        """
        
        :param first: 
        :param second: 
        :param op_func: 
        :param _: 
        :return: 
        """

        feature_tuple = tuple(feature_tuple)
        op_func_args = self._op_func_args(feature_tuple)

        result = 0
        try:
            result = self.op_func(*op_func_args)
        except ZeroDivisionError as ze:
            self.__logger.warning("ZeroDivisionError = %s on %s",
                                  ze,
                                  op_func_args)
        if self.op_func in self.BOOLEAN_OPERATORS:
            result = np.array(result, dtype=int)
        return result

    def _op_func_args(self, feature_tuple):
        seq = self._op_func_args_seq(feature_tuple)
        return tuple(seq)

    def _op_func_args_seq(self, feature_tuple):
        good_arg = self._filter_op_func_good_arg(feature_tuple)
        for feature in feature_tuple:
            if feature is None:
                feature = good_arg * 0.0
            yield feature

    @staticmethod
    def _filter_op_func_good_arg(args):
        for arg in args:
            if arg is not None:
                return arg
        return 0.0
