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

    UPDATE_KWARGS_METHODS_FUNC_NAME = 'update_kwargs_methods'
    UPDATE_KWARGS_FUNC_NAME = 'update_kwargs'

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

        update_kwargs_methods_func = getattr(
            result,
            mcs.UPDATE_KWARGS_METHODS_FUNC_NAME,
            None
        )

        update_kwargs_func = getattr(
            result,
            mcs.UPDATE_KWARGS_FUNC_NAME,
            None
        )

        if update_kwargs_methods_func:
            update_kwargs_methods = update_kwargs_methods_func()
            for method in update_kwargs_methods:
                if update_kwargs_func:
                    method_func = update_kwargs_func(method)
                    setattr(result, method.__name__, method_func)

        return result
