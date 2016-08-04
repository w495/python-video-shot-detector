# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import operator as op

import numpy as np

from .filter import Filter


class FilterOperator(Filter):
    __logger = logging.getLogger(__name__)

    def filter_objects(self, *args, **kwargs):
        kwargs.pop('operator', None)
        return super(FilterOperator, self).filter_objects(
            *args,
            **kwargs
        )

    def reduce_features_parallel(self,
                                 first,
                                 second,
                                 operator=None,
                                 *args, **kwargs):
        return self.apply_filter_operator(
            first,
            second,
            operator,
            *args,
            **kwargs
        )

    def apply_filter_operator(self,
                              first,
                              second,
                              operator=None,
                              is_right=False,
                              *args,
                              **kwargs):
        if is_right:
            return self._apply_filter_operator(
                second,
                first,
                operator,
                *args,
                **kwargs
            )
        return self._apply_filter_operator(
            first,
            second,
            operator,
            *args,
            **kwargs
        )

    def _apply_filter_operator(self,
                               first,
                               second,
                               operator=None,
                               *args, **kwargs):

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
            self.__logger.warn("ZeroDivisionError = %s %s %s",
                               ze,
                               first,
                               second)
        if operator in (op.lt, op.gt, op.le, op.ge, op.eq, op.ne):
            result = np.array(result, dtype=int)
        return result
