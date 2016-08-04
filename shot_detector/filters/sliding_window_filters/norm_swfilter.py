# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_swfilter import BaseSWFilter


class NormSWFilter(BaseSWFilter):
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.
        """
        min_size = 2
        strict_windows = False

    def aggregate_window_item(self, window, **kwargs):
        wlist = list(window)
        value = wlist[0]

        max_wlist = max(wlist)
        min_wlist = min(wlist)

        rng = max_wlist - min_wlist
        new_value = (value - min_wlist) / rng

        # print (value, new_value, max_wlist, min_wlist, wlist)

        return new_value
