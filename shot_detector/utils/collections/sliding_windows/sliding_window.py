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

from .repeated_sliding_window import RepeatedSlidingWindow


class SlidingWindow(RepeatedSlidingWindow):
    def __repr__(self):
        """
        Represents `SlidingWindow` as a string.

        :return string: representation
        """
        name = 'sw'
        return "{}({}, {})".format(
            name,
            list(self),
            self.window_size)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
