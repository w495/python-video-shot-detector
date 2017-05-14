# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function


from shot_detector.utils import ReprDict


class VideoTime(object):
    """
        ...
    """

    __slots__ = [
        'clock_time',
        'stream_time',
    ]

    initial_time = None

    def __init__(self, stream_time=None, clock_time=None):
        self.stream_time = stream_time
        self.clock_time = clock_time

    def __float__(self):
        return float(self.stream_time)


    def __repr__(self):
        return "{c} {s}".format(
            s=self.stream_time,
            c=self.clock_time
        )


    def repr_dict(self):
        repr_dict = ReprDict(type(self), self)
        return repr_dict