# -*- coding: utf8 -*-

from __future__ import absolute_import

from collections import OrderedDict

WINDOW_SIZE = 200
FLUSH_LIMIT = -1


class BaseSlidingWindowState(object):
    items = OrderedDict()
    item_counter = 0
    window_counter = 0
    window_size = WINDOW_SIZE
    flush_limit = FLUSH_LIMIT

    def __init__(self, window_size, *args, **kwargs):
        self.window_size = window_size
        self.flush_all()

    def values(self):
        return self.items.values()

    def update_items(self, item, window_size=WINDOW_SIZE):
        return self.store_items(
            item,
            self.get_window_counter(
                window_size
            )
        )

    @property
    def is_empty(self):
        return self.item_counter == 0

    @property
    def is_full(self):
        return self.window_size < self.item_counter

    def flush(self, flush_limit=FLUSH_LIMIT):
        if self.item_counter > self.flush_limit:
            self.flush_all()

    def flush_all(self):
        self.items = OrderedDict()
        self.item_counter = 0



    def get_window_counter(self, window_size=WINDOW_SIZE):
        self.window_size = window_size
        self.window_counter = self.item_counter
        if self.window_size:
            self.window_counter %= self.window_size
        self.item_counter += 1
        return self.window_counter

    def store_items(self, item, window_counter):
        self.items[window_counter] = item
        return self.items
