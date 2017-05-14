# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime


class Second(float):
    """
        ...
    """

    def timedelta(self):
        """
        
        :return: 
        """
        return datetime.timedelta(seconds=self)

    def hms(self):
        """
        
        :return: 
        """
        return str(self.timedelta())

    def minute(self):
        """
        
        :return: 
        """
        return self / 60.0

    def minsec(self):
        """
        
        :return: 
        """
        minute = int(self) // 60
        second = int(self) % 60
        return float("%s.%s" % (minute, second))
