# -*- coding: utf8 -*-
# pylint: disable=too-many-arguments

"""
    sliding (rolling) window module.

    If you apply sliding window with size='3' to
        [0, 1, 2, 3, 4, 5, 6, 7]
    you will get something like this
        [(0, 1, 2), (1, 2, 3),
            (2, 3, 4), (3, 4, 5),
                (4, 5, 6), (5, 6, 7)]
"""

from __future__ import absolute_import, division, print_function

import itertools

from .base_sliding_window import BaseSlidingWindow

DEFAULT_WINDOW_DELAY = 0


class DelayedSlidingWindow(BaseSlidingWindow):
    @classmethod
    def sliding_windows(cls,
                        sequence=(),
                        window_delay=DEFAULT_WINDOW_DELAY,
                        fill_d=0,
                        slice_d=0,
                        **kwargs):
        """

        :param collections.Iterable sequence:
            initial sequence of any element.
        :param int window_delay:
            offset from which window handling starts.
        :param kwargs:
        :return:
        """

        if window_delay:
            sequence = cls.rebuild_initial_sequence(
                sequence,
                window_delay,
                fill_d,
                slice_d
            )

        it_sequence = iter(sequence)

        # print (list(it_sequence))
        # delayed_sequence = itertools.islice(it_sequence,
        # window_delay, None)
        _sw_seq = super(DelayedSlidingWindow, cls).sliding_windows(
            sequence=it_sequence,
            **kwargs
        )
        #
        # from pprint import  pprint
        # pprint (list(tuple(sw) for sw in _sw_seq))

        return _sw_seq

    @classmethod
    def rebuild_initial_sequence(cls,
                                 sequence=(),
                                 window_delay=0,
                                 fill_d=0,
                                 slice_d=0
                                 ):
        for i in xrange(0 * window_delay):
            yield None

        it_sequence = iter(sequence)
        delayed_sequence = itertools.islice(it_sequence,
                                            window_delay,
                                            None)
        for item in delayed_sequence:
            yield item

    @classmethod
    def check_generator_parameters(cls,
                                   sequence=None,
                                   window_delay=None,
                                   **kwargs):

        super(DelayedSlidingWindow, cls).check_generator_parameters(
            sequence=sequence,
            **kwargs
        )


if __name__ == "__main__":
    dsw_seq = DelayedSlidingWindow.sliding_windows(xrange(10),
                                                   window_delay=10)

    print(list(tuple(sw) for sw in dsw_seq))

    import doctest

    doctest.testmod()
