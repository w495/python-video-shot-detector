# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .stat_test_swfilter import StatTestSWFilter

class QTestSWFilter(StatTestSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, window, **kwargs):


        self.get_max(window, **kwargs)

        self.get_min(window, **kwargs)


        return next(iter(window), None)
