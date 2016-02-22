# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .stat_swfilter import StatSWFilter


class MadSWFilter(StatSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, window_features, **kwargs):
        return self.get_mad(window_features, **kwargs)
