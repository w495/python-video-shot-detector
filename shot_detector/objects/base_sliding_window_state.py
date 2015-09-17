# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict

WINDOW_SIZE = 200

class BaseSlidingWindowState(object):

    items = {}
    point_counter  = 0
    window_counter = 0
    window_size    = WINDOW_SIZE
 
    def __init__(self, window_size, *args, **kwargs):
        self.window_size = window_size

    def values(self):
        return self.items.values()
            
    def update_items(self, items, window_size = WINDOW_SIZE):
        return self.store_items(
            items, 
            self.get_window_counter(
                window_size
            )
        )

    def get_window_counter(self, window_size = WINDOW_SIZE):
        self.window_size = window_size
        self.window_counter = self.point_counter
        if(self.window_size):
            self.window_counter %= self.window_size
        self.point_counter += 1
        return self.window_counter
    
    def store_items(self, items, window_counter):
        self.items[window_counter] = items
        return self.items
