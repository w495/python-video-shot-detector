# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import operator as op

import numpy as np

from .filter import Filter


class FilterOperator(Filter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def filter_objects(self, *args, **kwargs):
        """
        
        :param args: 
        :param kwargs: 
        :return: 
        """
        kwargs.pop('operator', None)
        return super(FilterOperator, self).filter_objects(
            *args,
            **kwargs
        )

    def reduce_features_parallel(self,
                                 feature_tuple,
                                 **kwargs):
        """
        
        :param first: 
        :param second: 
        :param operator: 
        :param args: 
        :param kwargs: 
        :return: 
        """


        return self.apply_filter_operator(
            feature_tuple,
            **kwargs
        )

    def apply_filter_operator(self,
                              feature_tuple,
                              is_right=False,
                              **kwargs):
        """
        
        :param first: 
        :param second: 
        :param operator: 
        :param is_right: 
        :param kwargs: 
        :return: 
        """

        if is_right:
            feature_tuple = reversed(feature_tuple)

        return self._apply_filter_operator(
            feature_tuple,
            **kwargs
        )

    def _apply_filter_operator(self,
                               feature_tuple,
                               operator=None,
                               **_):
        """
        
        :param first: 
        :param second: 
        :param operator: 
        :param _: 
        :return: 
        """

        first, second = feature_tuple

        if first is None and second is not None:
            first = second * 0
        if first is not None and second is None:
            second = first * 0
        if first is None and second is None:
            first = 0
            second = 0

        result = 0

        try:
            result = operator(first, second)
        except ZeroDivisionError as ze:
            self.__logger.warning("ZeroDivisionError = %s %s %s",
                                  ze,
                                  first,
                                  second)
        if operator in (op.lt, op.gt, op.le, op.ge, op.eq, op.ne):
            result = np.array(result, dtype=int)
        return result
