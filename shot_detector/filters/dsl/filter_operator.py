# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from enum import Enum

import logging
import operator

import numpy as np

from .dsl_nested_parallel_filter import DslNestedParallelFilter


class FilterOperator(DslNestedParallelFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    class Booleans(Enum):
        LT = operator.lt
        GT = operator.gt
        LE = operator.le
        GE = operator.ge
        EQ = operator.eq
        NE = operator.ne


    class Mode(Enum):
        LEFT = object()
        RIGHT = object()

    class Arity(Enum):
        BINARY = object()
        UNARY = object()

    op_arity = Arity.BINARY
    op_mode = Mode.LEFT

    def __init__(self,
                 op_func=None,
                 op_mode=None,
                 op_arity=None,
                 **kwargs):
        """
        
        :param op_func: 
        :param op_mode: 
        :param kwargs: 
        """
        self.op_func = op_func
        if op_mode:
            self.op_mode = op_mode
        if op_arity:
            self.op_arity = op_arity
        super(FilterOperator, self).__init__(**kwargs)

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
        result = 0
        try:
            result = self.apply_op_func(op_func_args)
        except ZeroDivisionError as ze:
            self.__logger.warning("%s on %s", ze, op_func_args)
        return result

    def apply_op_func(self, op_func_args):
        if self.op_arity is self.Arity.UNARY:
            result = self.op_func(op_func_args)
        else:
            result = self.op_func(*op_func_args)
        return result

    def handle_op_func_result(self, result):
        if self.op_func in self.Booleans:
            result = np.array(result, dtype=int)
        return result

    def prepare_op_func_args(self, feature_tuple):
        """
        
        :param feature_tuple: 
        :return: 
        """
        feature_tuple = tuple(feature_tuple)
        if self.op_mode is self.Mode.RIGHT:
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
