# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.features.filters.sliding_window_filters.base_swfilter import BaseSWFilter


class QTestSWFilter(BaseSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, window, **kwargs):
        return next(iter(window), None)
