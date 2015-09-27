# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from .base_combination_swfilter import BaseCombinationSWFilter
from .deviation_swfilter import DeviationSWFilter


class DeviationDifferenceSWFilter(DeviationSWFilter, BaseCombinationSWFilter):

    __logger = logging.getLogger(__name__)

    def combination(self, original_features, aggregated_features, *args, **kwargs):
        deviation = aggregated_features
        difference = original_features - deviation
        return difference
