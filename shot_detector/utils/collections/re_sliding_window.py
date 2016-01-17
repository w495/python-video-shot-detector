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

from .sliding_window import SlidingWindow

DEFAULT_WINDOW_SIZE = 4
DEFAULT_REPEAT_SIZE = 1


class ReSlidingWindow(SlidingWindow):
    @classmethod
    def sliding_windows(cls,
                        sequence=(),
                        window_size=DEFAULT_WINDOW_SIZE,
                        overlap_size=None,
                        yield_tail=False,
                        strict_windows=False,
                        repeat_windows=False,
                        repeat_size=None,
                        **kwargs):
        """

        :param collections.Iterable  sequence:
        :param int window_size:
        :param int overlap_size:
        :param bool yield_tail:
        :param bool strict_windows:
        :param bool repeat_windows:
        :param int repeat_size:
        :param dict kwargs: ignores it and pass it through
        :return :
        """

        _sw_seq = super(ReSlidingWindow, cls).sliding_windows(
            sequence=sequence,
            window_size=window_size,
            overlap_size=overlap_size,
            yield_tail=yield_tail,
            strict_windows=strict_windows,
            repeat_windows=repeat_windows,
            repeat_size=repeat_size,
            **kwargs
        )

        if repeat_windows and (repeat_size is None):
            repeat_size = window_size - overlap_size
        if (not repeat_windows) and (repeat_size is not None):
            repeat_windows = True

        if repeat_windows:
            sw_seq = cls.repeat_sliding_windows(
                _sw_seq,
                repeat_size,
                **kwargs
            )

        return _sw_seq

    @classmethod
    def check_generator_parameters(cls,
                                   sequence=None,
                                   window_size=None,
                                   overlap_size=None,
                                   yield_tail=None,
                                   strict_windows=None,
                                   repeat_windows=None,
                                   repeat_size=None,
                                   **kwargs):
        """
        Checks that all parameters has perfect types.

        :param collections.Iterable sequence:
            must be an iterable
        :param integer window_size:
            must be a positive integer
        :param integer overlap_size:
            must be a positive integer greater
            or equal to zero and less then `window_size`
            by default it is None
        :param boolean strict_windows:
            yield_tail must be in (True, False)
        :param boolean yield_tail:
            strict_windows must in (True, False)
        :param boolean repeat_windows:
            strict_windows must in (True, False)
        :param integer repeat_size:
            strict_windows must in (True, False)
        :raises TypeError and ValueError:
            raises if some of condition is wrong.

        """

        super(ReSlidingWindow, cls).check_generator_parameters(
            sequence=sequence,
            window_size=window_size,
            overlap_size=overlap_size,
            yield_tail=yield_tail,
            strict_windows=strict_windows,
            **kwargs
        )
        cls.ensure_type(
            repeat_windows, bool,
            'repeat_windows must be a bool')
        if repeat_size is not None:
            cls.ensure_type(
                repeat_size, (int, long),
                'repeat_size must be an int')
            cls.ensure_value(
                repeat_size, repeat_size >= 0,
                'repeat_size must be >= 0')

    @classmethod
    def repeat_sliding_windows(cls, sw_seq, repeat_size, **kwargs):
        """

        :param sw_seq:
        :param repeat_size:
        :return:
        """
        for window in sw_seq:
            window_copy_seq = itertools.tee(window, repeat_size)
            for window_copy in window_copy_seq:
                yield window_copy


if __name__ == '__main__':
    from pprint import pprint


    def tuple_list(seq):
        """
            Wraps SlidingWindow.sliding_windows
            to generate list of tuples instead of generator.
        """
        return list(tuple(sw) for sw in seq)


    sw_seq = ReSlidingWindow.sliding_windows(
        range(17),
        window_size=4,
        overlap_size=2,
        _windows=True,
        strict_windows=True,
    )

    tuples = tuple_list(sw_seq)

    pprint(tuples)
