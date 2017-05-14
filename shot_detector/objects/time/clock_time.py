# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime
from .base_time import BaseTime

class ClockTime(BaseTime):
    """
        ...
    """

    __slots__ = [
        'now',
        'time_delta',
        'timestamp',
        'time',
    ]

    initial_time = None

    def __init__(self):

        if not ClockTime.initial_time:
            ClockTime.initial_time = datetime.datetime.utcnow()

        self.now = datetime.datetime.utcnow()
        self.timestamp = self.now.timestamp()

        self.time_delta = self.now - ClockTime.initial_time

        self.time = self.time_delta.seconds
