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

from shot_detector.utils.collections import RepeatedSlidingWindow


class PointWindow(RepeatedSlidingWindow):
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

    @property
    def features(self):
        """
        :return:
        """
        return self.get_features()

    def get_features(self, **_):
        """

        :param _:
        :return:
        """
        for item in iter(self):
            if hasattr(item, 'feature'):
                yield item.feature


if __name__ == "__main__":
    import doctest

    doctest.testmod()
