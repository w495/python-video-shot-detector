# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_nested_filter import BaseNestedFilter


class FilterDifference(BaseNestedFilter):
    __logger = logging.getLogger(__name__)

    def reduce_parallel(self, first, second, *args):
        # print ('first, second ', first, second, args)
        return first - second
