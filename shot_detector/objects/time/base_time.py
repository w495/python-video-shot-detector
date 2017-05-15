# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from shot_detector.utils import ReprDict


class BaseTime(object):
    """
        ...
    """

    __slots__ = [
        'time',
        'time_delta',
    ]

    def __float__(self):
        """
        
        :return: 
        """
        return float(self.time)

    def __int__(self):
        """
        
        :return: 
        """
        return float(self.time)

    def __repr__(self):
        """
        
        :return: 
        """
        return "{td}".format(
            td=self.time_delta,
        )

    def repr_dict(self):
        """
        
        :return: 
        """
        repr_dict = ReprDict(type(self), self)
        return repr_dict
