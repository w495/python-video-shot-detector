# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from .base_combination_swfilter import BaseCombinationSWFilter


class DifferenceSWFilter(BaseCombinationSWFilter):

    __logger = logging.getLogger(__name__)

    def combine_feature_item(self, original_feature, aggregated_feature, **kwargs):
        difference = original_feature - aggregated_feature
        return difference
