# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function


class BaseFrameSize(object):
    def __init__(self, width=0, height=0):
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
