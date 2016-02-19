# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .stat_swfilter import StatSWFilter


class NikitinSWFilter(StatSWFilter):

    __logger = logging.getLogger(__name__)


    def aggregate_windows(self,
                          window_seq,
                          **kwargs):


        for window in window_seq:
            mean = self.get_mean(window, **kwargs)

            upper = list(item for item in window if item > mean)
            lower = list(item for item in window if item <= mean)



            upper_mean =  self.get_mean(upper)
            lower_mean =  self.get_mean(lower)


            yield upper_mean / lower_mean - 1
