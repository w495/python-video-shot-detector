# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_swfilter import BaseSWFilter

class PackSWFilter(BaseSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, sequence, to_filter=None, **_):
        if to_filter:
            return self.seq_to_filter(sequence)
        return sequence