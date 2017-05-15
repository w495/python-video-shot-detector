# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import functools

import six

from shot_detector.utils import UpdateKwargsWrapper


class NotNoneKwDefaultsObject(six.with_metaclass(UpdateKwargsWrapper)):
    """
        ...
    """

    @classmethod
    def update_kwargs_methods(cls):
        """
        
        :return: 
        """
        return [
            cls.__init__
        ]

    @classmethod
    def update_kwargs_handler(cls, method):
        """
        
        :param method: 
        :return: 
        """

        defaults = getattr(method, '__kwdefaults__', dict())
        if defaults:
            @functools.wraps(method)
            def new_func(*args, **kwargs):
                """
                
                :param args: 
                :param kwargs: 
                :return: 
                """
                real_dict = dict(kwargs)
                for key, value in six.iteritems(kwargs):
                    if value is None:
                        real_dict[key] = defaults.get(key)
                return method(*args, **real_dict)

            return new_func
        return method
