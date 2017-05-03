# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class StdSWFilter(BaseStatSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, features, **kwargs):
        features = self.try_ignore_last(features, **kwargs)
        return self.get_std(features, **kwargs)

    def try_ignore_last(self, features, ignore_last=False, **kwargs):
        if ignore_last:
            features = list(features)[:-1]
        return features
