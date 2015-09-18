# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict

WINDOW_SIZE = 200
FLUSH_LIMIT = 25

class BaseSlidingWindowState(object):

    items = {}
    item_counter  = 0
    window_counter = 0
    window_size   = WINDOW_SIZE
    flush_limit   = FLUSH_LIMIT
    
 
    def __init__(self, window_size, *args, **kwargs):
        self.window_size = window_size
        self.items = {}
        self.item_counter = 0


    def values(self):
        return self.items.values()
            
    def update_items(self, items, window_size = WINDOW_SIZE):
        return self.store_items(
            items, 
            self.get_window_counter(
                window_size
            )
        )
    @property
    def is_empty(self):
        return self.item_counter == 0

    def flush(self, flush_limit = FLUSH_LIMIT):
        if self.item_counter > self.flush_limit:
            self.items = {}
            self.item_counter = 0

    @property
    def is_full(self):
        return self.window_size < self.item_counter

    def get_window_counter(self, window_size = WINDOW_SIZE):
        self.window_size = window_size
        self.window_counter = self.item_counter
        if(self.window_size):
            self.window_counter %= self.window_size
        self.item_counter += 1
        return self.window_counter
    
    def store_items(self, items, window_counter):
        self.items[window_counter] = items
        return self.items
