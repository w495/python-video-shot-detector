# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .filter import Filter


class FilterIntersection(Filter):

    __logger = logging.getLogger(__name__)

    def reduce_parallel(self,
                        first,
                        second,
                        threshold=0,
                        *args,
                        **kwargs):

        min_ = min(first, second)
        max_ = max(first, second)

        if min_ == threshold:
            return min_
        return max_
