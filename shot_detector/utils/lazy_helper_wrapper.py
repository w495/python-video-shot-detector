# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging


class LazyHelperWrapper(type):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    handlers = [
        ('update_kwargs_methods', 'update_kwargs_handler')
    ]

    def __new__(mcs, class_name=None, bases=None, dict=None, **_):
        """
        
        :param class_name: 
        :param bases: 
        :param attr_dict: 
        :return: 
        """

        result = super(LazyHelperWrapper, mcs).__new__(
            mcs,
            class_name,
            bases,
            dict
        )

        for methods_name, handler_name in mcs.handlers:
            methods_func = getattr(
                result,
                methods_name,
                None
            )

            handler_func = getattr(
                result,
                handler_name,
                None
            )

            if methods_func:
                update_kwargs_methods = methods_func()
                for method in update_kwargs_methods:
                    if handler_func:
                        method_func = handler_func(method)
                        setattr(result, method.__name__, method_func)

        return result
