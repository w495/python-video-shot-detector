# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime


class TimeFloat(float):
    """
        ...
    """

    def td(self):
        """
        
        :return: 
        """
        td = datetime.timedelta(
            seconds=self
        )

        td.total_seconds()
        return td

    def hms(self):
        """
        
        :return: 
        """
        td = self.td()
        str_td = str(td)
        return str_td

    def mns(self):
        """
        
        :return: 
        """

        minute = int(self) // 60
        second = int(self) % 60
        minute_second = "%s.%s" % (minute, second)
        human_minute = float(minute_second)
        return human_minute

    def minute(self):
        """

        :return: 
        """
        return self / 60.0
