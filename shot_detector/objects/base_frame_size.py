# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function


class BaseFrameSize(object):
    """
        ...
    """
    def __init__(self, width=0, height=0):
        """
        
        :param width: 
        :param height: 
        """
        self.__width = width
        self.__height = height

    @property
    def width(self):
        """
        
        :return: 
        """
        return self.__width

    @property
    def height(self):
        """
        
        :return: 
        """
        return self.__height
