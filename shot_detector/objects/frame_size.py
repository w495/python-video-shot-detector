# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from shot_detector.utils import ReprDict


class FrameSize(object):
    """
        ...
    """

    __slots__ = [
        'width',
        'height'
    ]

    def __init__(self, width=None, height=None):
        """
        
        :param width: 
        :param height: 
        """
        self.width = width
        self.height = height

    def __repr__(self):
        """
        
        :return: 
        """
        return "{w}x{h}".format(w=self.width, h=self.height)

    def repr_dict(self):
        """
        
        :return: 
        """
        repr_dict = ReprDict(type(self), self)
        return repr_dict
