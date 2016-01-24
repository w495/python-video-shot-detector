# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_nested_filter import BaseNestedFilter


class FilterOperator(BaseNestedFilter):

    __logger = logging.getLogger(__name__)

    def reduce_parallel(self, first, second, operator, *args, **kwargs):

        if first is None and second is not None:
            first = second * 0
        if first is not None and second is None:
            second = first * 0
        if first is None and second is None:
            first = 0
            second = 0


        return operator(first, second)

    def filter_feature_item(self,
                            feature,
                            other=None,
                            operator=None,
                            **kwargs):
        return operator(feature, other)