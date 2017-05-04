# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function


class BaseNorm(object):
    """
        ...
    """
    def norm(self, vector, **kwargs):
        """
        
        :param vector: 
        :param kwargs: 
        :return: 
        """
        length = self.__class__.length(vector, **kwargs)
        return length

    @classmethod
    def length(cls, vector, **kwargs):
        """
        
        :param vector: 
        :param kwargs: 
        :return: 
        """
        raise NotImplementedError('length')
