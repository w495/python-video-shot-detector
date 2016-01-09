# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import datetime


class Second(float):
    def timedelta(self):
        return datetime.timedelta(seconds=self)

    def hms(self):
        return str(self.timedelta())

    def minute(self):
        return self / 60.0

    def minsec(self):
        minute = int(self) // 60
        second = int(self) % 60
        return float("%s.%s" % (minute, second))
