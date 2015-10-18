# -*- coding: utf8 -*-

from __future__ import absolute_import

from collections import OrderedDict
from collections import deque


WINDOW_SIZE = 200
FLUSH_LIMIT = -1


class BaseSlidingWindow(object):

    items = None
    window_size = WINDOW_SIZE
    flush_limit = FLUSH_LIMIT

    def __init__(self, window_size = None, *args, **kwargs):
        if window_size is not None:
            self.window_size = window_size
        self.items = deque([], self.window_size)

    def values(self):
        return list(self.items)

    def push(self, item, window_size=None, *args, **kwargs):
        if window_size is not None:
            self.window_size = window_size

        if self.window_size > self.items.maxlen:
            self.items = deque(self.items, self.window_size)

        self.items.appendleft(item)
        return self.items

    @property
    def is_empty(self):
        return len(self.items) == 0

    @property
    def is_full(self):
        return len(self.items) == self.items.maxlen

    def flush(self, flush_limit=None, window_size=None, *args, **kwargs):
        if flush_limit is not None:
           self.flush_limit = flush_limit
        if window_size is not None:
            self.window_size = window_size
        if len(self.items) > self.flush_limit:
            self.items = deque([], self.window_size)


