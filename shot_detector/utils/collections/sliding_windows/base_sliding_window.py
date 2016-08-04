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

    How to use is see the doc of:
        SlidingWindow.sliding_windows
"""

from __future__ import absolute_import, division, print_function

import collections
import itertools

import six

DEFAULT_WINDOW_SIZE = 2


class BaseSlidingWindow(collections.deque):
    """
    Implements deque-based  sliding (rolling) window behaviour.

    If you apply sliding window with size='3' to
        [0, 1, 2, 3, 4, 5, 6, 7]
    you will get something like this
        [(0, 1, 2), (1, 2, 3),
            (2, 3, 4), (3, 4, 5),
                (4, 5, 6), (5, 6, 7)]

    How to use is see the doc of:
        SlidingWindow.sliding_windows
    """

    # the maximum size of sliding window instance.
    window_size = None

    def __init__(self, sequence=(), window_size=None, **kwargs):
        # noinspection PyPep8,PyTypeChecker
        """
        Creates deque-based SlidingWindow instance.

        :param collections.Iterable sequence:
            initial sequence for sliding
        :param int window_size:
            size of the sliding window; if the it less then
            sequence size, output sequence will be reduced
            to the sliding window size from the end.
        :param dict kwargs:
            dict for sub class parameters,
            ignores it and pass it through
        :returns SlidingWindow:
            one sliding window instance

        :raises TypeError: parameters has wrong types.
        :raises ValueError: parameters has wrong types.

        >>> BaseSlidingWindow(range(1), window_size=2)
        BaseSlidingWindow([0], 2)
        >>> BaseSlidingWindow(range(2), window_size=2)
        BaseSlidingWindow([0, 1], 2)
        >>> BaseSlidingWindow(range(3), window_size=2)
        BaseSlidingWindow([1, 2], 2)
        >>> BaseSlidingWindow(range(10), window_size=3)
        BaseSlidingWindow([7, 8, 9], 3)
        >>> BaseSlidingWindow(10, window_size=3)
        Traceback (most recent call last):
                ...
        TypeError: sequence must be an iterable; has int
        >>> BaseSlidingWindow(range(10), window_size=3.1)
        Traceback (most recent call last):
                ...
        TypeError: window_size must be an int; has float
        >>> BaseSlidingWindow(range(10), window_size=-1)
        Traceback (most recent call last):
                ...
        ValueError: window_size must be > 0; has -1

        """
        type(self).check_init_parameters(
            sequence,
            window_size,
            **kwargs
        )

        self.window_size = window_size
        super(BaseSlidingWindow, self).__init__(
            sequence,
            maxlen=window_size)

    def __repr__(self):
        """
        Represents `SlidingWindow` as a string.

        :return string: representation
        """
        name = type(self).__name__
        return "{}({}, {})".format(
            name,
            list(self),
            self.window_size)

    @classmethod
    def sliding_windows(cls,
                        sequence=(),
                        window_size=DEFAULT_WINDOW_SIZE,
                        overlap_size=None,
                        min_size=None,
                        yield_tail=False,
                        strict_windows=False,
                        **kwargs):
        # noinspection PyPep8,PyTypeChecker
        """
        Generates a sequence of sliding windows over a `sequence`.

        It expects that a sequence (second parameter)
        is an `iterable` and returns a `generator object`.
        By default the size of the each window is 2,
        but you can specify it with a `window_size` (third) parameter.
        Each window implements a `collections.deque` interface.

        How can you use it?
        Let define initial sequence and function for uncovering
        the generator content to a tuple list.

        >>> sequence = xrange(8)
        >>> list(sequence)
        [0, 1, 2, 3, 4, 5, 6, 7]
        >>> sw_gen = BaseSlidingWindow.sliding_windows
        >>> def sliding_windows(*args, **kwargs):
        ...     return list(
        ...         tuple(sw)
        ...         for sw in sw_gen(*args, **kwargs)
        ...     )
        ...

        Default behaviour: Number of input items equals
        to number of output ones. This is not right sliding windows,
        but it is very useful for many applications.

        >>> default = sliding_windows(sequence)
        >>> default
        [(0,), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
        >>> len(sequence) == len(default)
        True
        >>> soft_sw_list_2 = sliding_windows(sequence, window_size=2)
        >>> soft_sw_list_2
        [(0,), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
        >>> len(sequence) == len(soft_sw_list_2)
        True
        >>> soft_sw_list_3 = sliding_windows(sequence, window_size=3)
        >>> soft_sw_list_3
        [(0,), (0, 1), (0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7)]
        >>> len(sequence) == len(soft_sw_list_3)
        True

        It implements more accurate behaviour
        with `strict_windows` parameter.

        >>> strict_sw_list_2 = sliding_windows(
        ...     sequence,
        ...     window_size=2,
        ...     strict_windows=True
        ... )
        ...
        >>> strict_sw_list_2
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
        >>> len(sequence)
        8
        >>> len(strict_sw_list_2)
        7
        >>> strict_sw_list_3 = sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     strict_windows=True
        ... )
        >>> strict_sw_list_3
        [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7)]
        >>> len(sequence)
        8
        >>> len(strict_sw_list_3)
        6
        >>> strict_sw_list_4 = sliding_windows(
        ...     sequence,
        ...     window_size=4,
        ...     strict_windows=True
        ... )
        >>> strict_sw_list_4
        [(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (4, 5, 6, 7)]
        >>> len(sequence)
        8
        >>> len(strict_sw_list_4)
        5

        Also you can overlap windows.
        By default windows overlapped with (window_size - 1) elements.

        >>> strict_lapped_default = sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     strict_windows=True
        ... )
        ...
        >>> strict_lapped_default
        [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7)]
        >>> strict_lapped_3_2 = sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     overlap_size=2,
        ...     strict_windows=True
        ... )
        ...
        >>> strict_lapped_3_2
        [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7)]
        >>> strict_lapped_3_1 = sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     overlap_size=1,
        ...     strict_windows=True
        ... )
        ...
        >>> strict_lapped_3_1
        [(0, 1, 2), (2, 3, 4), (4, 5, 6)]

        The same you can do with «soft» sliding windows.
        Note that overlapping do not work on the incomplete windows
        (at the start of window sequence). It needs
        to accumulate the full window before applying overlapping.

        >>> soft_lapped_3_1 = sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     overlap_size=1,
        ...     strict_windows=False
        ... )
        ...
        >>> soft_lapped_3_1
        [(0,), (0, 1), (0, 1, 2), (2, 3, 4), (4, 5, 6)]

        Look at the end of the `soft_lapped_3_1`. There is no `7`.
        It has happened because 7 — the last member of initial sequence
        and it do not fit with overlapping scheme.
        For this case you can use `yield_tail` parameter.
        There are two ways to generate tail of
            [(0, 1, 2), (2, 3, 4), (4, 5, 6)]
        One is
            [(0, 1, 2), (2, 3, 4), (4, 5, 6), (5, 6, 7)]
        And other is
            [(0, 1, 2), (2, 3, 4), (4, 5, 6), (7,)]
        We decide that constant size of window is more important.

        >>> strict_lapped_3_1_tail = sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     overlap_size=1,
        ...     yield_tail=True,
        ...     strict_windows=True
        ... )
        ...
        >>> strict_lapped_3_1_tail
        [(0, 1, 2), (2, 3, 4), (4, 5, 6), (5, 6, 7)]

        The same you can do with «soft» sliding windows.

        >>> strict_lapped_3_1_tail = sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     overlap_size=1,
        ...     yield_tail=True,
        ...     strict_windows=False
        ... )
        ...
        >>> strict_lapped_3_1_tail
        [(0,), (0, 1), (0, 1, 2), (2, 3, 4), (4, 5, 6), (5, 6, 7)]

        This is not recommended case of use. It is quite difficult
        to understand the logic of the last example looking only on
        the result.

        If you set `overlap_size` to zero you will get partitions
        of initial sequence. This is degenerate case of sliding windows.

        >>> sliding_windows(
        ...     sequence,
        ...     window_size=2,
        ...     overlap_size=0,
        ...     strict_windows=True
        ...     )
        [(0, 1), (2, 3), (4, 5), (6, 7)]
        >>> sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     overlap_size=0,
        ...     strict_windows=True
        ... )
        [(0, 1, 2), (3, 4, 5)]
        >>> sliding_windows(
        ...     sequence,
        ...     window_size=4,
        ...     overlap_size=0,
        ...     strict_windows=True
        ... )
        [(0, 1, 2, 3), (4, 5, 6, 7)]
        >>> sliding_windows(
        ...     sequence, window_size=5,
        ...     overlap_size=0,
        ...     strict_windows=True
        ... )
        [(0, 1, 2, 3, 4)]

        As you guess, you can use `yield_tail` in this case too.

        >>> sliding_windows(
        ...     sequence,
        ...     window_size=2,
        ...     overlap_size=0,
        ...     yield_tail=True,
        ...     strict_windows=True
        ... )
        [(0, 1), (2, 3), (4, 5), (6, 7)]
        >>> sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     overlap_size=0,
        ...     yield_tail=True,
        ...     strict_windows=True
        ... )
        [(0, 1, 2), (3, 4, 5), (5, 6, 7)]
        >>> sliding_windows(
        ...     sequence,
        ...     window_size=4,
        ...     overlap_size=0,
        ...     yield_tail=True,
        ...     strict_windows=True
        ... )
        [(0, 1, 2, 3), (4, 5, 6, 7)]
        >>> sliding_windows(
        ...     sequence, window_size=5,
        ...     overlap_size=0,
        ...     yield_tail=True,
        ...     strict_windows=True
        ... )
        [(0, 1, 2, 3, 4), (3, 4, 5, 6, 7)]

        With «soft sliding windows», partitions are also «soft».
        As it was shown before, it needs to accumulate
        the full partition item by item.

        >>> sliding_windows(
        ...     sequence,
        ...     window_size=2,
        ...     overlap_size=0,
        ...     strict_windows=False
        ... )
        [(0,), (0, 1), (2, 3), (4, 5), (6, 7)]
        >>> sliding_windows(
        ...     sequence,
        ...     window_size=3,
        ...     overlap_size=0,
        ...     strict_windows=False
        ... )
        [(0,), (0, 1), (0, 1, 2), (3, 4, 5)]
        >>> sliding_windows(
        ...     sequence,
        ...     window_size=4,
        ...     overlap_size=0,
        ...     strict_windows=False
        ... )
        [(0,), (0, 1), (0, 1, 2), (0, 1, 2, 3), (4, 5, 6, 7)]
        >>> sliding_windows(
        ...     sequence,
        ...     window_size=5,
        ...     overlap_size=0,
        ...     strict_windows=False
        ... )
        [(0,), (0, 1), (0, 1, 2), (0, 1, 2, 3), (0, 1, 2, 3, 4)]

        If you deal with finite sequences and set
        the window size greater than sequence size
        you will get some strange effects.
        It is also not recommended case of use.

        >>> finite_sequence = (0, 1, 2, 3)
        >>> sliding_windows(
        ...     finite_sequence,
        ...     window_size=10,
        ...     strict_windows=False
        ... )
        [(0,), (0, 1), (0, 1, 2), (0, 1, 2, 3)]
        >>> sliding_windows(
        ...     finite_sequence,
        ...     window_size=10,
        ...     strict_windows=True
        ... )
        []
        >>> sliding_windows(
        ...     finite_sequence,
        ...     window_size=10,
        ...     strict_windows=True,
        ...     yield_tail=True,
        ... )
        [(0, 1, 2, 3)]

        For fool-tolerance you cannot set `window_size`
        and `overlap_size` to the same number,
        because it doesn't make sense.

        >>> sliding_windows(sequence, window_size=3, overlap_size=3)
        Traceback (most recent call last):
            ...
        ValueError: overlap_size must be < window_size; has (3, 3)

        In this case you should get:
            [(0,), (0, 1), (0, 1, 2), (0, 1, 2), (0, 1, 2), (0, 1, 2),
            ... an infinite number of times ... ]
        You can achieve this much more simpler
        without sliding windows =). You will get the same with
        overlap size greater then window size.

        >>> sliding_windows(sequence, window_size=3, overlap_size=42)
        Traceback (most recent call last):
            ...
        ValueError: overlap_size must be < window_size; has (42, 3)

        The size of window should be a positive number.

        >>> sliding_windows(sequence, window_size=0)
        ...
        Traceback (most recent call last):
            ...
        ValueError: window_size must be > 0; has 0

        >>> sliding_windows(sequence, window_size=-42)
        ...
        Traceback (most recent call last):
            ...
        ValueError: window_size must be > 0; has -42


        The overlap size should be be a positive number or null.

        >>> sliding_windows(sequence, overlap_size=-1)
        ...
        Traceback (most recent call last):
            ...
        ValueError: overlap_size must be >= 0; has -1

        Also it controls types of arguments:

        >>> sliding_windows(42)
        Traceback (most recent call last):
            ...
        TypeError: sequence must be an iterable; has int
        >>> sliding_windows(sequence, 2.1)
        Traceback (most recent call last):
            ...
        TypeError: window_size must be an int; has float
        >>> sliding_windows(sequence, 'abc')
        Traceback (most recent call last):
            ...
        TypeError: window_size must be an int; has str
        >>> sliding_windows(sequence, 2, 1.1)
        Traceback (most recent call last):
            ...
        TypeError: overlap_size must be an int; has float
        >>> sliding_windows(sequence, 2, yield_tail=0)
        Traceback (most recent call last):
            ...
        TypeError: yield_tail must be a bool; has int
        >>> sliding_windows(sequence, 2, strict_windows=0)
        Traceback (most recent call last):
            ...
        TypeError: strict_windows must be a bool; has int

        To sum up all examples, this is formal specification.

        :param collections.Iterable sequence:
            initial sequence of any element.
        :param int window_size:
            size of each sliding window;
            window_size have to be greater than zero.
        :param int overlap_size: number
            number of overlapping items in sliding windows;
            by default overlap_size = (window_size - 1)
        :param int min_size: number
            minimal size of non-strict window;
            it sets flag `strict_windows` to True.
        :param bool strict_windows:
            flag to form sliding windows with the same size
            each other; otherwise at first it generates windows
            during accumulating items;
            by default `strict_windows` is False.
        :param bool yield_tail:
            flag to generate the rest of sequence
            that do not match to overlapping scheme.
            by default `yield_tail` is False.
        :param dict kwargs:
            dict for sub class parameters,
            ignores it and pass it through

        :returns: <generator object sliding_windows at ... >
            Do not forget about it. If you want to use the result
            of this functions several times you should apply
            itertools.tee or convert this generator
            to concrete objects.
        :raises TypeError and ValueError:
            if parameters has wrong types and values.

        """

        cls.check_generator_parameters(
            sequence=sequence,
            window_size=window_size,
            overlap_size=overlap_size,
            yield_tail=yield_tail,
            strict_windows=strict_windows,
            **kwargs
        )

        if overlap_size is None:
            overlap_size = window_size - 1

        win = cls(window_size=window_size)
        append = win.append

        win_min_size = window_size
        if min_size:
            win_min_size = min_size
            strict_windows = True

        yield_cond = None
        skip_limit = window_size - overlap_size
        skip_counter = 0
        for item_index, item in enumerate(sequence):
            skip_counter += 1
            append(item)
            skip_cond = (skip_counter < skip_limit)
            head_cond = item_index < window_size
            yield_cond = head_cond or (not skip_cond)
            if strict_windows:
                head_cond = item_index >= (win_min_size - 1)
                yield_cond = head_cond and (not skip_cond)
            if yield_cond:
                yield win
                skip_counter = 0
        if yield_tail and not yield_cond:
            yield win

    @classmethod
    def check_generator_parameters(cls,
                                   sequence=None,
                                   window_size=None,
                                   overlap_size=None,
                                   yield_tail=None,
                                   strict_windows=None,
                                   **kwargs):
        """
        Checks that all parameters has perfect types.

        :param collections.Iterable sequence:
            must be an iterable
        :param int window_size:
            must be a positive int
        :param int overlap_size:
            must be a positive int greater
            or equal to zero and less then `window_size`
            by default it is None
        :param bool strict_windows:
            yield_tail must be in (True, False)
        :param bool yield_tail:
            strict_windows must in (True, False)
        :param dict kwargs:
            dict for sub class parameters,
            ignores it and pass it through
        :raises TypeError and ValueError:
            raises if some of condition is wrong.
        """

        cls.check_init_parameters(
            sequence=sequence,
            window_size=window_size,
            **kwargs
        )

        cls.ensure_type(
            yield_tail, bool,
            'yield_tail must be a bool')

        cls.ensure_type(
            strict_windows, bool,
            'strict_windows must be a bool')

        if overlap_size is not None:
            cls.ensure_type(
                overlap_size, six.integer_types,
                'overlap_size must be an int')
            cls.ensure_value(
                overlap_size, overlap_size >= 0,
                'overlap_size must be >= 0')
            cls.ensure_value(
                (overlap_size, window_size),
                overlap_size < window_size,
                'overlap_size must be < window_size'
            )

    @classmethod
    def check_init_parameters(cls,
                              sequence=None,
                              window_size=None,
                              **_):
        """
        Checks that all parameters has perfect types.

        :param collections.Iterable sequence: must be an iterable
        :param int window_size: must be a positive int
        :param dict _: dict for sub class parameters, ignores it.
        :returns None:
        :raises TypeError and ValueError:
            if some of condition is wrong.

        """
        cls.ensure_type(
            sequence, collections.Iterable,
            'sequence must be an iterable')
        cls.ensure_type(
            window_size, six.integer_types,
            'window_size must be an int')
        cls.ensure_value(
            window_size, window_size > 0,
            'window_size must be > 0')

    def __getitem__(self, index):
        """
        Implements self[index] behaviour.

        It overloads only one case from base class (deque):
        iterate over it in with itertools.

        :param Any index: any index for get item
        :return: item from part of initial sequence
            that gets into SlidingWindow
        """
        if isinstance(index, slice):
            i_slice = itertools.islice(self, index.start,
                                       index.stop, index.step)
            return type(self)(i_slice, window_size=self.window_size)
        return super(BaseSlidingWindow, self).__getitem__(index)

    @classmethod
    def ensure_value(cls, value, condition, message='error'):
        """
        Checks condition and raises ValueError if it is wrong.

        Raised ValueError has `message` with current `value`.
        It looks like:
            ValueError("{message}; has {value}")

        :param Any value: any value;
        :param bool condition: condition to check;
        :param str message: part of message for ValueError;
        :raises ValueError: if `condition` is wrong.

        """
        cls.assert_value(
            condition,
            '{}; has {}'.format(
                message,
                value
            )
        )

    @classmethod
    def assert_value(cls, condition=False, message='error'):
        """
        Checks condition and raises ValueError if it is wrong

        :param bool condition: condition to check;
        :param string message: message for `ValueError(message)`
        :raises ValueError: if `condition` is wrong.
        """

        cls._assert(condition, ValueError(message))

    @classmethod
    def ensure_type(cls, value, types, message='error'):
        """
        Checks that `value` is instance of `types`.

        If it is wrong and raises TypeError with
        `message` and name of current value type.
        It looks like: `TypeError("{message}; has {type(value)}")`.

        :param Any value: value to check types;
        :param type or tuple types: types for checking;
        :param  str message: part of message for `TypeError`;
        :raises TypeError: if `condition` is wrong.
        """

        cls.assert_type(
            isinstance(value, types),
            '{}; has {}'.format(
                message,
                type(value).__name__
            )
        )

    @classmethod
    def assert_type(cls, condition=False, message='error'):
        """
        Checks condition and raises TypeError if it is wrong.

        :param bool condition: condition to check;
        :param string message: message for `TypeError(message)`
        :raises TypeError: if `condition` is wrong.

        """
        cls._assert(condition, TypeError(message))

    @staticmethod
    def _assert(condition=False, exception=Exception, message=None):
        """
        Checks condition and raises exception if it is wrong.

        :param bool condition: condition to check;
        :param BaseException exception: raised exception;
        :param str message: message for `exception(message)`;
        :raises exception: if `condition` is wrong.
        """
        if message is None:
            exc = exception
        else:
            exc = exception(message)
        if not condition:
            raise exc


if __name__ == "__main__":
    import doctest

    doctest.testmod()
