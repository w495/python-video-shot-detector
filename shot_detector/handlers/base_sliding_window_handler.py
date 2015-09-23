# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import uuid

import os
import thread
        
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
    window_name = None

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
        
        self.window_name = id(self)
        #print ('self.__window_name = ', self.window_name)
        return self.window_name

    def get_window_state(self, video_state, *args, **kwargs):
        window_name = self.get_window_name(*args, **kwargs)
        window_state = video_state.sliding_windows.get(window_name)
        return window_state
    
    def set_window_state(self, video_state, window_state, *args, **kwargs):
        window_name = self.get_window_name(*args, **kwargs)
        video_state.sliding_windows[window_name] = window_state
        return window_state   
    
    def flush_window_state(self, video_state, *args, **kwargs):
        window_state = self.get_window_state(
            video_state, 
            *args, **kwargs
        )
        flush_limit = self.get_flush_limit(*args, **kwargs)
        window_state.flush(flush_limit)
        return None

    @staticmethod
    def get_flush_limit(*args, **kwargs):
        return kwargs.pop('flush_limit', FLUSH_LIMIT)

    @staticmethod
    def get_window_size(*args, **kwargs):
        return kwargs.pop('window_size', WINDOW_SIZE)

    def build_window_state(self, window_size = None, *args, **kwargs):
        window_size = self.get_window_size(window_size = window_size, *args, **kwargs)
        window_state = BaseSlidingWindowState(
            window_size = window_size, 
            *args, 
            **kwargs
        )
        return window_state

    def update_window_state(self, items, window_state, *args, **kwargs):
        window_size = self.get_window_size(*args, **kwargs)
        window_state.update_items(items, window_size)
        return window_state
