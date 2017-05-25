# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from functools import partial

import six


class CliEscapePainter(object):
    """
        ...
    """

    def __init__(self, **kwargs):
        for name, value in six.iteritems(kwargs):
            new_color = partial(CliEscapePainter.as_str, value)
            setattr(self, name, new_color)

    @staticmethod
    def as_str(color_func, string=None, *args, **kwargs):
        """

        :param color_func: 
        :param string: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        obj = color_func(string=string, *args, **kwargs)
        return str(obj)
