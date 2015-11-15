# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals


from collections import deque
from itertools import islice


WINDOW_SIZE = 200
FLUSH_LIMIT = -1


class SlidingWindow(deque):

    @staticmethod
    def windows(iterable, window_size=2):
        win = SlidingWindow([], maxlen=window_size)
        append = win.append
        for item in iterable:
            append(item)
            yield win

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(islice(self, index.start, index.stop, index.step))
        return super(SlidingWindow, self).__getitem__(index)

