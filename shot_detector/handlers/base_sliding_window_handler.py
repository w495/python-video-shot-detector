# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging


from shot_detector.objects import BaseSlidingWindowState



WINDOW_SIZE = 200

class BaseSlidingWindowHandler(object):

    __logger = logging.getLogger(__name__)

    def init_window_state(self, video_state = None, window_name = __name__, 
                          *args, **kwargs):
        window_state = video_state.sliding_windows.get(window_name)
        if not window_state:
            window_state = \
                video_state.sliding_windows[window_name] = \
                    self.build_window_state(*args, **kwargs)
        return window_state

    def build_window_state(self, window_size = WINDOW_SIZE, *args, **kwargs):
        window_state = BaseSlidingWindowState(
            window_size = window_size, 
            *args, 
            **kwargs
        )
        return window_state

    def update_window_state(self, items, window_state, window_size = WINDOW_SIZE, *args, **kwargs):
        window_state.update_items(items, window_size)
        return window_state
