# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime
import time
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
            ClockTime.initial_time = time.time()
        self.now = time.time()
        _time = self.now - ClockTime.initial_time
        self.time = _time
        self.time_delta = datetime.timedelta(
            seconds=_time
        )