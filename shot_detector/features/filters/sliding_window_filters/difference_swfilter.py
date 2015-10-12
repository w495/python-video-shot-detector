# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from .base_combination_swfilter import BaseCombinationSWFilter


class DifferenceSWFilter(BaseCombinationSWFilter):

    __logger = logging.getLogger(__name__)

    def combination(self, original_features, aggregated_features, *args, **kwargs):
        difference = original_features - aggregated_features
        return difference
