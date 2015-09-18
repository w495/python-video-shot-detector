# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from shot_detector.objects import BaseSlidingWindowState

##
## Default size of sliding window
##
WINDOW_SIZE = 200


##
## Minmal size of sliding window, when it can be flushed.
##
FLUSH_LIMIT = 100

class BaseSlidingWindowHandler(object):

    __logger = logging.getLogger(__name__)

    def init_window_state(self, video_state, *args, **kwargs):
        """
            Creates sliding window and set it as a part of video_state.
            If window already exists — do nothing.
            In any case, this function returns current window
        """
        wstate = self.get_window_state(video_state, *args, **kwargs)
        if not wstate:
            wstate = self.build_window_state(*args, **kwargs)
            self.set_window_state(
                video_state, 
                wstate, 
                *args, **kwargs
            )
        return wstate

    def get_window_name(self, *args, **kwargs):
        window_name = id(self)
        return window_name

    def get_window_state(self, video_state, *args, **kwargs):
        window_name = self.get_window_name(*args, **kwargs)
        window_state = video_state.sliding_windows.get(window_name)
        return window_state
    
    def set_window_state(self, video_state, window_state, *args, **kwargs):
        window_name = self.get_window_name(*args, **kwargs)
        video_state.sliding_windows[window_name] = window_state
        return window_state   
    
    def flush_window_state(self, 
                           video_state, 
                           flush_limit = FLUSH_LIMIT,  
                           *args, **kwargs
                           ):
        window_state = self.get_window_state(
            video_state, 
            *args, **kwargs
        )
        window_state.flush(flush_limit)
        return None
        
    def build_window_state(self, window_size = WINDOW_SIZE, *args, **kwargs):
        window_state = BaseSlidingWindowState(
            window_size = window_size, 
            *args, 
            **kwargs
        )
        return window_state

    def update_window_state(self, 
                            items, 
                            window_state, 
                            window_size = WINDOW_SIZE, 
                            *args, **kwargs):
        window_state.update_items(items, window_size)
        return window_state
