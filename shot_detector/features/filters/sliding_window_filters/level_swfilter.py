# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class LevelSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self,
                              sequence=(),
                              level_number=10,
                              **kwargs):
        """

        :param list sequence:
        :param int level_number:
        :param dict kwargs:
        :return:
        """
        local_max = self.local_max(sequence, **kwargs)
        local_mim = self.local_min(sequence, **kwargs)
        width = (local_max - local_mim)
        bin_width = width / level_number
        level = 0
        current = sequence[0]
        for step in xrange(level_number):
            left = local_mim + bin_width * step
            right = local_mim + bin_width * (step + 1)
            if left <= current <= right:
                level = step / level_number
                break

        return level

    def local_max(self,
                  sequence,
                  global_max=None,
                  **kwargs):
        """

        :param collections.Iterable sequence:
        :param int global_max:
        :param dict  kwargs:
        :return:
        """
        local_max = global_max
        if local_max is None:
            local_max = self.get_max(sequence, **kwargs)
        return local_max

    def local_min(self,
                  sequence,
                  global_min=None,
                  **kwargs):
        """

        :param collections.Iterable sequence:
        :param int global_min:
        :param dict kwargs:
        :return:
        """
        local_min = global_min
        if local_min is None:
            local_min = self.get_min(sequence, **kwargs)
        return local_min
