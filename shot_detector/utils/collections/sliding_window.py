# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from collections import deque
from itertools import islice
from itertools import tee

WINDOW_SIZE = 200
FLUSH_LIMIT = -1


class SlidingWindow(deque):

    # @classmethod
    # def sliding_windows2(cls, sequence, window_size=2, overlap_size=2):
    #     sw_seq = SlidingWindow.sliding_windows(sequence, window_size)
    #
    #     for sw in sw_seq:
    #         for item in sequence:
    #



    @classmethod
    def sliding_windows(cls, sequence, window_size=2, overlap_size=None):
        """
        
        :param sequence: 
        :param window_size: 
        :return: 

        """
        if overlap_size is None:
            overlap_size = window_size - 1

        win = SlidingWindow([], maxlen=window_size)
        append = win.append
        for index, item in enumerate(sequence):
            print ('index = ', index % window_size, item)


            append(item)
            if not index % (window_size - overlap_size):
                yield win

    @classmethod
    def tuple_seq(cls, sw_seq):
        for sw in sw_seq:
            yield tuple(sw)

    @classmethod
    def tuple(cls, sw_seq):
        return tuple(cls.tuple_seq(sw_seq))


    @staticmethod
    def groups(sequence, window_size=2, reuse=1):

        if reuse == 1:
            sequence1, sequence2 = tee(sequence)
            while True:
                win = SlidingWindow(islice(sequence1, window_size), maxlen=window_size)
                win.number = 0
                if not len(win):
                    break

                yield win

        if reuse == 2:
            win = SlidingWindow([], maxlen=window_size)
            append = win.append
            win.number = 0

            while True:
                sl = islice(sequence, window_size)
                s1, s2 = tee(sl)
                for item in s1:
                    append(item)
                for _ in s2:
                    yield win
                else:
                    break

        if reuse == 3:
            win = SlidingWindow([], maxlen=window_size)
            win.number = 0

            append = win.append
            for item in sequence:
                append(item)
                yield win

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(islice(self, index.start, index.stop, index.step))
        return super(SlidingWindow, self).__getitem__(index)

def test():
    sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sw = SlidingWindow.sliding_windows(sequence,3,1)
    print (SlidingWindow.tuple(sw))




if __name__ == '__main__':
    test()

