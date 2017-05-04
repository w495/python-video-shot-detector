# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function

import logging

from .filter import Filter


class JoinFilter(Filter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def __call__(self, a, b, **kwargs):
        """
        
        :param a: 
        :param b: 
        :param kwargs: 
        :return: 
        """
        return a.join(b)
