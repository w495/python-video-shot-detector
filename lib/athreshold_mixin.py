# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np
import logging

class AThresholdMixin(object):

    __logger = logging.getLogger(__name__)

    def handle_difference(self, value, video_state, window_size = 200, window_limit = 50, *args, **kwargs):

        if(not video_state.video_window):
            video_state.video_window = {}
            video_state.frame_counter = 0

        win_counter = video_state.frame_counter
        if(window_size):
            win_counter = win_counter % window_size

        video_state.video_window[win_counter] = value * 1.0
        video_state.frame_counter += 1

        if(not window_limit):
            window_limit = 1


        video_window = np.array(video_state.video_window.values())
        value_mean = video_window.mean()


        '''
            More effective  way
        if(1 == win_counter):
            video_state.value_mean = value
        else:
            video_state.value_mean = (value + video_state.value_mean * (win_counter - 1)) / win_counter
        '''

        value_std = video_window.std()


        athresold = value_mean  + 3 * value_std

        if(athresold < value and win_counter > window_limit):
            self.__logger.debug("%s sec = %s value = %s,  %s [%s]"%(
                video_state.curr.time.time(),
                video_state.curr.time,
                value,
                athresold,
                video_state.frame_counter
            ))

            video_state.cut_list += [video_state.curr]
            video_state.cut_counter += 1
            video_state.frame_counter = 0
            video_state.video_window = {}

        return video_state


