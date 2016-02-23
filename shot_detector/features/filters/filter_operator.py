# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import operator as op
import numpy as np

from .filter import Filter

class FilterOperator(Filter):

    __logger = logging.getLogger(__name__)

    def reduce_features_parallel(self,
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
        if operator == op.div or operator == op.truediv:
            if 0 == second:
                return first * 0
        result = operator(first, second)
        if operator in (op.lt, op.gt, op.le, op.ge, op.eq, op.ne):
            result = np.array(result, dtype=int)
        return result

    def filter_feature_item(self,
                            feature,
                            other=None,
                            operator=None,
                            **kwargs):
        return self.reduce_features_parallel(feature, other,
                                             operator, **kwargs)