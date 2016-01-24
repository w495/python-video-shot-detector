# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .filter import Filter

class FilterDifference(Filter):

    __logger = logging.getLogger(__name__)

    def reduce_parallel(self, first, second, *args, **kwargs):
        return first - second
