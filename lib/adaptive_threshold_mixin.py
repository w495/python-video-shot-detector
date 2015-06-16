# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np
import logging


from .base_compare_mixin import BaseCompareMixin

class AdaptiveThresholdMixin(BaseCompareMixin):

    __logger = logging.getLogger(__name__)

    def handle_difference(self, value, video_state, sigma_num = 3,
                          window_size = 100, window_limit = 40, comp_func = np.all,
                          *args, **kwargs):

        if(not window_limit):
            window_limit = 1

        if(not video_state.video_window):
            video_state.video_window = {}
            video_state.frame_counter = 0

        win_counter = video_state.frame_counter
        if(window_size):
            win_counter = win_counter % window_size

        video_window = np.array(video_state.video_window.values())
        value_mean   = video_window.mean(axis = 0)
        value_std    = video_window.std(axis = 0)
        thresold_max = value_mean + sigma_num * value_std

        if comp_func(value >= thresold_max) and (win_counter > window_limit):
            self.__logger.debug("%s sec = %s value = %s,  %s [%s]"%(
                video_state.curr.time.time(),
                video_state.curr.time,
                np.sum(value),
                np.sum(thresold_max),
                video_state.frame_counter
            ))

            video_state.cut_list += [video_state.curr]
            video_state.cut_counter += 1
            video_state.frame_counter = 0
            video_state.video_window = {}

        video_state.video_window[win_counter] = value * 1.0
        video_state.frame_counter += 1

        return video_state


