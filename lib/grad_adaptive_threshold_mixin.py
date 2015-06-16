# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np
import logging


from .base_compare_mixin import BaseCompareMixin

class GradAdaptiveThresholdMixin(BaseCompareMixin):

    __logger = logging.getLogger(__name__)

    def handle_difference(self, value, video_state, sigma_num = 3,
                          window_size = 2000, window_limit = 50, comp_func = np.all,
                          *args, **kwargs):

        if(not window_limit):
            window_limit = 1

        if(not video_state.video_window):
            video_state.video_window = {}
            video_state.frame_counter = 0
            video_state.lvalue = [value, value]

        win_counter = video_state.frame_counter
        if(window_size):
            win_counter = win_counter % window_size


        if len(video_state.video_window) > 2:

            video_window = np.gradient(np.array(video_state.video_window.values()))
            value_mean   = video_window.mean(axis = 0)
            value_std    = video_window.std(axis = 0)

            video_state.lvalue = [video_state.lvalue[-1], value]
            gvalue = np.gradient(video_state.lvalue)[0]

            thresold_max = value_mean  + sigma_num * value_std

            if comp_func(gvalue >= thresold_max) and (win_counter > window_limit):
                self.__logger.debug("gr %s sec = %s value = %s,  %s [%s]"%(
                    video_state.curr.time.time(),
                    video_state.curr.time,
                    np.sum(gvalue),
                    thresold_max,
                    video_state.frame_counter
                ))
                video_state.cut_list += [video_state.curr]
                video_state.cut_counter += 1
                video_state.video_window = {}
                video_state.frame_counter = 0

        video_state.video_window[win_counter] = value * 1.0
        video_state.frame_counter += 1

        return video_state


