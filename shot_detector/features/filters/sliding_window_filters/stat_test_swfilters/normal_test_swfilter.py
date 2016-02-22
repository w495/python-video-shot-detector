# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.features.filters.sliding_window_filters.scipy_stat_swfilter import SciPyStatSWFilter


class NormalTestSWFilter(SciPyStatSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, features, **kwargs):
        normaltest_result = self.normaltest(features, **kwargs)
        return normaltest_result.pvalue

