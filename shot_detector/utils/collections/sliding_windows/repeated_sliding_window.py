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

DEFAULT_WINDOW_SIZE = 4
DEFAULT_REPEAT_SIZE = 1


class RepeatedSlidingWindow(BaseSlidingWindow):
    """
    Very similar to SlidingWindow but `ReSlidingWindow.sliding_windows`
    has two external parameters `repeat_windows` and `repeat_size`
    If `repeat_windows` or `repeat_size` are set it «reslides»
    parts of initial sequence under each window.
    """

    @classmethod
    def sliding_windows(cls,
                        sequence=(),
                        window_size=DEFAULT_WINDOW_SIZE,
                        overlap_size=None,
                        repeat_windows=False,
                        repeat_size=None,
                        **kwargs):
        # noinspection PyPep8,PyTypeChecker
        """
        Does the same SlidingWindow.sliding_windows but repeat windows.

        If `repeat_windows` or `repeat_size` are set it «reslides»
        parts of initial sequence under each window.


        :param collections.Iterable sequence:
            initial sequence of any element.
        :param int window_size:
            size of each sliding window;
            window_size have to be greater than zero.
        :param int overlap_size: number
            number of overlapping items in sliding windows;
            by default overlap_size = (window_size - 1)
        :param bool repeat_windows:
            launch the «repeat functionality»; sets repeat_size to
            `repeat_size = window_size - overlap_size`;
            by default is not set.
            must be bool.
        :param int repeat_size:
            how many times repeat each window;
            by default is not set,
            but if `repeat_windows is True`
            `repeat_size = window_size - overlap_size`;
            must be an integer or None for default.
        :param dict kwargs: ignores it and pass it through.

        :returns: <generator object sliding_windows at ... >
            Do not forget about it. If you want to use the result
            of this functions several times you should apply
            itertools.tee or convert this generator
            to concrete objects.
        :rtype: collections.Iterable[ReSlidingWindow]

        :raises TypeError and ValueError:
            raises if some of condition is wrong.

        Let define initial sequence and function for uncovering
        the generator content to a tuple list.

        >>> from pprint import  pprint
        >>> sequence = xrange(23)
        >>> pprint(list(sequence))
        [0,
         1,
         2,
         3,
         4,
         5,
         6,
         7,
         8,
         9,
         10,
         11,
         12,
         13,
         14,
         15,
         16,
         17,
         18,
         19,
         20,
         21,
         22]
        >>> sw_gen = RepeatedSlidingWindow.sliding_windows
        >>> def sliding_windows(*args, **kwargs):
        ...     return list(
        ...         tuple(sw)
        ...         for sw in sw_gen(*args, **kwargs)
        ...     )
        >>> soft_sw_8 = sliding_windows(
        ...    sequence,
        ...    window_size=8
        ... )
        >>> pprint(soft_sw_8)
        [(0,),
         (0, 1),
         (0, 1, 2),
         (0, 1, 2, 3),
         (0, 1, 2, 3, 4),
         (0, 1, 2, 3, 4, 5),
         (0, 1, 2, 3, 4, 5, 6),
         (0, 1, 2, 3, 4, 5, 6, 7),
         (1, 2, 3, 4, 5, 6, 7, 8),
         (2, 3, 4, 5, 6, 7, 8, 9),
         (3, 4, 5, 6, 7, 8, 9, 10),
         (4, 5, 6, 7, 8, 9, 10, 11),
         (5, 6, 7, 8, 9, 10, 11, 12),
         (6, 7, 8, 9, 10, 11, 12, 13),
         (7, 8, 9, 10, 11, 12, 13, 14),
         (8, 9, 10, 11, 12, 13, 14, 15),
         (9, 10, 11, 12, 13, 14, 15, 16),
         (10, 11, 12, 13, 14, 15, 16, 17),
         (11, 12, 13, 14, 15, 16, 17, 18),
         (12, 13, 14, 15, 16, 17, 18, 19),
         (13, 14, 15, 16, 17, 18, 19, 20),
         (14, 15, 16, 17, 18, 19, 20, 21),
         (15, 16, 17, 18, 19, 20, 21, 22)]
        >>> strict_sw_8 = sliding_windows(
        ...     sequence,
        ...     window_size=8,
        ...     strict_windows=True
        ... )
        >>> pprint(strict_sw_8)
        [(0, 1, 2, 3, 4, 5, 6, 7),
         (1, 2, 3, 4, 5, 6, 7, 8),
         (2, 3, 4, 5, 6, 7, 8, 9),
         (3, 4, 5, 6, 7, 8, 9, 10),
         (4, 5, 6, 7, 8, 9, 10, 11),
         (5, 6, 7, 8, 9, 10, 11, 12),
         (6, 7, 8, 9, 10, 11, 12, 13),
         (7, 8, 9, 10, 11, 12, 13, 14),
         (8, 9, 10, 11, 12, 13, 14, 15),
         (9, 10, 11, 12, 13, 14, 15, 16),
         (10, 11, 12, 13, 14, 15, 16, 17),
         (11, 12, 13, 14, 15, 16, 17, 18),
         (12, 13, 14, 15, 16, 17, 18, 19),
         (13, 14, 15, 16, 17, 18, 19, 20),
         (14, 15, 16, 17, 18, 19, 20, 21),
         (15, 16, 17, 18, 19, 20, 21, 22)]

        >>> strict_sw_8_overlap_6 = sliding_windows(
        ...     sequence,
        ...     window_size=8,
        ...     overlap_size=6,
        ...     strict_windows=True
        ... )
        >>> pprint(strict_sw_8_overlap_6)
        [(0, 1, 2, 3, 4, 5, 6, 7),
         (2, 3, 4, 5, 6, 7, 8, 9),
         (4, 5, 6, 7, 8, 9, 10, 11),
         (6, 7, 8, 9, 10, 11, 12, 13),
         (8, 9, 10, 11, 12, 13, 14, 15),
         (10, 11, 12, 13, 14, 15, 16, 17),
         (12, 13, 14, 15, 16, 17, 18, 19),
         (14, 15, 16, 17, 18, 19, 20, 21)]
        >>>
        >>> len(sequence)
        23
        >>> len(soft_sw_8)
        23
        >>> len(strict_sw_8)
        16
        >>> len(strict_sw_8_overlap_6)
        8

        Sequence of windows with big overlap is dramatically smaller.
        In some applications it is not convenient. This solves
        with `repeat_windows` parameter. Each window are copied
        certain number of times. By default this number is
        `window_size - overlap_size`.

        >>> strict_sw_8_overlap_6_repeat = sliding_windows(
        ...     sequence,
        ...     window_size=8,
        ...     overlap_size=6,
        ...     repeat_windows=True,
        ...     strict_windows=True
        ... )
        >>> pprint(strict_sw_8_overlap_6_repeat)
        [(0, 1, 2, 3, 4, 5, 6, 7),
         (0, 1, 2, 3, 4, 5, 6, 7),
         (2, 3, 4, 5, 6, 7, 8, 9),
         (2, 3, 4, 5, 6, 7, 8, 9),
         (4, 5, 6, 7, 8, 9, 10, 11),
         (4, 5, 6, 7, 8, 9, 10, 11),
         (6, 7, 8, 9, 10, 11, 12, 13),
         (6, 7, 8, 9, 10, 11, 12, 13),
         (8, 9, 10, 11, 12, 13, 14, 15),
         (8, 9, 10, 11, 12, 13, 14, 15),
         (10, 11, 12, 13, 14, 15, 16, 17),
         (10, 11, 12, 13, 14, 15, 16, 17),
         (12, 13, 14, 15, 16, 17, 18, 19),
         (12, 13, 14, 15, 16, 17, 18, 19),
         (14, 15, 16, 17, 18, 19, 20, 21),
         (14, 15, 16, 17, 18, 19, 20, 21)]
        >>> len(strict_sw_8_overlap_6)
        8
        >>> len(strict_sw_8_overlap_6_repeat)
        16

        By default number of window copies is
        `window_size - overlap_size`. But you can specify it whit
        `repeat_size` parameter. If `repeat_size` is set,
        `repeat_windows` is not required.

        >>> strict_sw_8_overlap_6_repeat_3 = sliding_windows(
        ...     sequence,
        ...     window_size=8,
        ...     overlap_size=6,
        ...     repeat_size=3,
        ...     strict_windows=True
        ... )
        >>> pprint(strict_sw_8_overlap_6_repeat_3)
        [(0, 1, 2, 3, 4, 5, 6, 7),
         (0, 1, 2, 3, 4, 5, 6, 7),
         (0, 1, 2, 3, 4, 5, 6, 7),
         (2, 3, 4, 5, 6, 7, 8, 9),
         (2, 3, 4, 5, 6, 7, 8, 9),
         (2, 3, 4, 5, 6, 7, 8, 9),
         (4, 5, 6, 7, 8, 9, 10, 11),
         (4, 5, 6, 7, 8, 9, 10, 11),
         (4, 5, 6, 7, 8, 9, 10, 11),
         (6, 7, 8, 9, 10, 11, 12, 13),
         (6, 7, 8, 9, 10, 11, 12, 13),
         (6, 7, 8, 9, 10, 11, 12, 13),
         (8, 9, 10, 11, 12, 13, 14, 15),
         (8, 9, 10, 11, 12, 13, 14, 15),
         (8, 9, 10, 11, 12, 13, 14, 15),
         (10, 11, 12, 13, 14, 15, 16, 17),
         (10, 11, 12, 13, 14, 15, 16, 17),
         (10, 11, 12, 13, 14, 15, 16, 17),
         (12, 13, 14, 15, 16, 17, 18, 19),
         (12, 13, 14, 15, 16, 17, 18, 19),
         (12, 13, 14, 15, 16, 17, 18, 19),
         (14, 15, 16, 17, 18, 19, 20, 21),
         (14, 15, 16, 17, 18, 19, 20, 21),
         (14, 15, 16, 17, 18, 19, 20, 21)]
        >>> len(strict_sw_8_overlap_6_repeat_3)
        24

        >>> sliding_windows(
        ...     sequence,
        ...     window_size=8,
        ...     repeat_windows=0,
        ... )
        Traceback (most recent call last):
            ...
        TypeError: repeat_windows must be a bool; has int

        >>> sliding_windows(
        ...     sequence,
        ...     window_size=8,
        ...     repeat_size=1.1,
        ... )
        Traceback (most recent call last):
            ...
        TypeError: repeat_size must be an int; has float
        >>> sliding_windows(
        ...     sequence,
        ...     window_size=8,
        ...     repeat_size=-11,
        ... )
        Traceback (most recent call last):
            ...
        ValueError: repeat_size must be >= 0; has -11

        """

        _sw_seq = super(RepeatedSlidingWindow, cls).sliding_windows(
            sequence=sequence,
            window_size=window_size,
            overlap_size=overlap_size,
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
                                   repeat_windows=None,
                                   repeat_size=None,
                                   **kwargs):
        """
        Checks that all parameters has perfect types.

        :param sequence:
            must be an iterable
        :param boolean repeat_windows:
            strict_windows must in (True, False)
        :param integer repeat_size:
            strict_windows must in (True, False)
        :param dict kwargs: ignores it and pass it through.
        :raises TypeError and ValueError:
            raises if some of condition is wrong.

        """

        super(RepeatedSlidingWindow, cls).check_generator_parameters(
            sequence=sequence,
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

        :param collections.Iterable[BaseSlidingWindow] sw_seq:
            sequence of sliding windows.
        :param int repeat_size: numbers to repeat each window;
        :param dict _: dict for sub class parameters, ignores it.
        :rtype: collections.Iterable[RepeatedSlidingWindow]
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
