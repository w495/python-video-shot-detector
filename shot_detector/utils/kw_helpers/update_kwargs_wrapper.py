# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging


class UpdateKwargsWrapper(type):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    # they should be class methods!
    handlers = [
        ('update_kwargs_methods', 'update_kwargs_handler')
    ]

    def __new__(mcs, class_name=None, bases=None, dict_=None, **_):
        """
        Creates and patches created class with decorated methods.
        
        Note:
            Here we operate class methods, so
            we cannot decorate methods, before class is created.
            After class construction it patches new class
            with decorated methods.
            
        :param class_name: 
        :param bases: 
        :param attr_dict: 
        :return: 
        """

        result = super(UpdateKwargsWrapper, mcs).__new__(
            mcs,
            class_name,
            bases,
            dict_
        )

        for methods_name, handler_name in mcs.handlers:
            methods_getter = getattr(result, methods_name, None)
            handler_func = getattr(result, handler_name, None)
            if isinstance(handler_func, str):
                handler_func = dict_[handler_func]
            if methods_getter and handler_func:
                methods_for_update = mcs.apply_getter(methods_getter)
                for method in methods_for_update:
                    if isinstance(method, str):
                        method = dict_[method]
                    method_func = handler_func(method)
                    setattr(result, method.__name__, method_func)

        return result

    @staticmethod
    def apply_getter(value):
        """
        
        :param value: 
        :return: 
        """
        if callable(value):
            return value()
        return value
