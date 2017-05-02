# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .scipy_stat_swfilter import SciPyStatSWFilter


class SkewnessSWFilter(SciPyStatSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, features, **kwargs):
        describe_result = self.describe(features, **kwargs)
        return describe_result.skewness
