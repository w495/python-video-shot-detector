# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime

from .base_time import BaseTime


class StreamTime(BaseTime):
    """
        ...
    """

    __slots__ = [
        'time_delta',
        'sec',
        'time_base',
        'pts',
        'dts',
    ]

    def __init__(self,
                 sec=None,
                 time_base=None,
                 pts=None,
                 dts=None, ):
        self.time_base = time_base
        self.pts = pts
        self.dts = dts
        self.sec = sec
        self.time_delta = datetime.timedelta(
            seconds=sec
        )

    def __repr__(self):
        """

        :return: 
        """
        string = (
            "{{"
            "pts:{pts:d},"
            "dts:{dts:d},"
            "sec:{sec:f},"
            'time:"{time}"'
            "}}".format(
                pts=self.pts,
                dts=self.dts,
                sec=self.sec,
                time=self.time_delta
            )
        )
        return string
