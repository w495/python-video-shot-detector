# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals


from collections import deque
from itertools import islice
from itertools import tee


from itertools import count
from itertools import groupby




WINDOW_SIZE = 200
FLUSH_LIMIT = -1


class SlidingWindow(deque):

    @staticmethod
    def sliding_windows(iterable, window_size=2):
        win = SlidingWindow([], maxlen=window_size)
        append = win.append
        for item in iterable:
            append(item)
            yield win


    @staticmethod
    def groups(iterable, window_size=2, reuse = 1):

        if reuse == 1:
            iterable1, iterable2 = tee(iterable, 2)
            while True:
                win = SlidingWindow(islice(iterable1, window_size), maxlen=window_size)
                win.number = 0
                if not len(win):
                    break


                yield win


        if reuse == 2:
            win = SlidingWindow([], maxlen=window_size)
            append = win.append
            win.number = 0

            while True:
                sl = islice(iterable, window_size)
                s1, s2 = tee(sl, 2)
                for item in s1:
                    append(item)


                for item in s2:
                    yield win
                else:
                    break



        if reuse == 3:
            win = SlidingWindow([], maxlen=window_size)
            win.number = 0

            append = win.append
            for item in iterable:
                append(item)
                yield win



    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(islice(self, index.start, index.stop, index.step))
        return super(SlidingWindow, self).__getitem__(index)

