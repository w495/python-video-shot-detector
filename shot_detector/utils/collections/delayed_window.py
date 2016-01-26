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

DEFAULT_WINDOW_DELAY = 0
DEFAULT_WINDOW_SIZE = 4




class DelayedWindow(SlidingWindow):


    @classmethod
    def sliding_windows(cls,
                        sequence=(),
                        window_size=DEFAULT_WINDOW_SIZE,
                        window_delay=DEFAULT_WINDOW_DELAY,
                        overlap_size=None,
                        yield_tail=False,
                        strict_windows=False,
                        repeat_windows=False,
                        repeat_size=None,
                        **kwargs):


        _sw_seq = super(DelayedWindow, cls).sliding_windows(
            sequence=sequence,
            window_size=window_size,
            overlap_size=overlap_size,
            yield_tail=yield_tail,
            strict_windows=strict_windows,
            repeat_windows=repeat_windows,
            repeat_size=repeat_size,
            **kwargs
        )

        if overlap_size is None:
            overlap_size = window_size - 1
        if repeat_windows and (repeat_size is None):
            repeat_size = window_size - overlap_size
        if (not repeat_windows) and (repeat_size is not None):
            repeat_windows = True

        if repeat_windows:
            _sw_seq = cls.repeat_sliding_windows(
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

        :param sequence:
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
        :param dict kwargs: ignores it and pass it through.
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
    def repeat_sliding_windows(cls,
                               sw_seq=(),
                               repeat_size=1,
                               **_):
        """
        Copies each sliding window `repeat_size` times.

        :param collections.Iterable[SlidingWindow] sw_seq:
            sequence of sliding windows.
        :param int repeat_size: numbers to repeat each window;
        :param dict _: dict for sub class parameters, ignores it.
        :rtype: collections.Iterable[ReSlidingWindow]
        :returns: <generator object sliding_windows at ... >
            Do not forget about it. If you want to use the result
            of this functions several times you should apply
            itertools.tee or convert this generator
            to concrete objects.
        """
        for window in sw_seq:
            for window_copy in itertools.tee(window, repeat_size):
                yield cls(window_copy, window.window_size)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
