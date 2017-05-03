# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_swfilter import BaseSWFilter


class ShiftSWFilter(BaseSWFilter):
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.
        """
        window_size = 2
        strict_windows = False
        cs = False

    def aggregate_window_item(self, window, **kwargs):
        return next(iter(window), None)
