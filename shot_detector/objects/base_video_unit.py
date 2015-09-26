# -*- coding: utf8 -*-

from __future__ import absolute_import

from shot_detector.utils.collections import SmartDict

from .second import Second


class BaseVideoUnit(SmartDict):

    source = None

    __time = None

    @property
    def time(self):
        if self.__time is None:
            if self.source and self.source.time:
                self.__time = Second(self.source.time)
        return self.__time

    @property
    def hms(self):
        if self.__time:
            return self.__time.hms()
        return 0

    @property
    def global_number(self):
        if self.source:
            return self.source.global_number
        return 0

    @property
    def number(self):
        return self.global_number
