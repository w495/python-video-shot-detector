# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import operator
from enum import Enum
from functools import reduce

import numpy as np

from .dsl_nested_parallel_filter import DslNestedParallelFilter


class FilterOperatorBooleans(Enum):
    """
        Booleans       
    """

    LT = operator.lt
    GT = operator.gt
    LE = operator.le
    GE = operator.ge
    EQ = operator.eq
    NE = operator.ne


class FilterOperatorMode(Enum):
    """
        Direction of operations        
    """
    LEFT = operator.lshift
    RIGHT = operator.rshift


class FilterOperator(DslNestedParallelFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    op_func = operator.eq
    op_mode = FilterOperatorMode.LEFT

    def reduce_features_parallel(self, feature_tuple, **kwargs):
        """

        :param feature_tuple: 
        :param kwargs: 
        :return: 
        """

        return self.reduce_with_op_func(feature_tuple, **kwargs)

    def reduce_with_op_func(self, feature_tuple, **kwargs):
        """

        :param feature_tuple: 
        :param kwargs: 
        :return: 
        """

        op_func_args = self.prepare_op_func_args(feature_tuple)
        result = self.try_op_func(op_func_args)
        result = self.handle_op_func_result(result)
        return result

    def try_op_func(self, op_func_args):
        """
        
        :param op_func_args: 
        :return: 
        """
        result = 0
        try:
            result = reduce(self.op_func, op_func_args)
        except ZeroDivisionError as ze:
            self.__logger.warning("%s on %s", ze, op_func_args)
        return result

    def handle_op_func_result(self, result):
        """
        
        :param result: 
        :return: 
        """
        if self.op_func in FilterOperatorBooleans:
            result = np.array(result, dtype=int)
        return result

    def prepare_op_func_args(self, feature_tuple):
        """

        :param feature_tuple: 
        :return: 
        """
        feature_tuple = tuple(feature_tuple)
        if self.op_mode is FilterOperatorMode.RIGHT:
            feature_tuple = reversed(feature_tuple)
        seq = self.prepare_op_func_args_seq(feature_tuple)
        return tuple(seq)

    def prepare_op_func_args_seq(self, feature_tuple):
        """

        :param feature_tuple: 
        :return: 
        """
        good_arg = self._filter_op_func_good_arg(feature_tuple)
        for feature in feature_tuple:
            if feature is None:
                feature = good_arg * 0.0
            yield feature

    @staticmethod
    def _filter_op_func_good_arg(args):
        """

        :param args: 
        :return: 
        """
        for arg in args:
            if arg is not None:
                return arg
        return 0.0

    def __eq__(self, other):
        """

        :param Any other: 
        :return: 
        """

        op_func = None
        op_mode = None

        if isinstance(other, FilterOperator):
            op_func = other.op_func
            op_mode = other.op_mode

        if isinstance(other, dict):
            op_func = other['op_func']
            op_mode = other['op_mode']

        if isinstance(other, tuple):
            op_func, op_mode = other

        same_op_func = (self.op_func == op_func)
        same_op_mode = (self.op_mode == op_mode)
        is_same = same_op_func and same_op_mode
        return is_same
