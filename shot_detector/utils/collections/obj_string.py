# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

class ObjString(str):
    """
        ...
    """


    def __init__(self, *_):
        super(ObjString, self).__init__()


    def __add__(self, other):
        """

        :param str | ObjString other: 
        :return: 
        """
        return ObjString(self + other)

    def __radd__(self, other):
        """

        :param str | ObjString other: 
        :return: 
        """
        return ObjString(other + self)