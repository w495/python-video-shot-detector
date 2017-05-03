# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.features.norms import L1Norm
from .base_swfilter import BaseSWFilter


class FFMpegLikeTresholdSWFilter(BaseSWFilter):
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.

            Sets the minimal size for sliding window.
        """
        window_size = 3
        min_size = 2
        strict_windows = True

    def aggregate_windows(self,
                          window_seq,
                          **kwargs):
        prev_mafd = 1
        for window in window_seq:
            prev = window[0]
            curr = window[1]
            diff = (curr - prev)
            mafd = L1Norm.length(diff, use_abs=True)

            mafd_diff = abs(mafd - prev_mafd)

            result = min(mafd, mafd_diff)
            prev_mafd = mafd
            yield result



            # def aggregate_window_item(self, window, **kwargs):
            #     prev = next(iter(window), None)
            #     curr = next(iter(window), None)
            #     if self.prev_mafd is None:
            #        self.prev_mafd = 0 * curr
            #     mafd = (curr - prev)
            #     ret = min(mafd, self.prev_mafd)
            #     self.prev_mafd = mafd
            #     return ret
