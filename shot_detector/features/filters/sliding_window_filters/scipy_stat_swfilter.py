# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from scipy import stats

from .base_swfilter import BaseSWFilter


class SciPyStatSWFilter(BaseSWFilter):

    __logger = logging.getLogger(__name__)

    def describe(self, features, **kwargs):
        return stats.describe(features)
