# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_test_swfilter import BaseStatTestSWFilter


class NormalTestSWFilter(BaseStatTestSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, features, **kwargs):
        normaltest_result = self.normaltest(features, **kwargs)
        return normaltest_result.pvalue
