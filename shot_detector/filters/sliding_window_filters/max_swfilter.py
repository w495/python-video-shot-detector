# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class MaxSWFilter(BaseStatSWFilter):
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.
        """
        strict_windows = False

    def aggregate_window_item(self, window_features, **kwargs):
        return self.get_max(window_features, **kwargs)
