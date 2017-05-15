# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime
from collections import Sequence, Set, Mapping
from enum import Enum
from types import BuiltinFunctionType, FunctionType
from uuid import UUID

import six
from numpy import ndarray

from .frozen_map import FrozenMap


class FrozenDict(FrozenMap):
    """
        ...
    """

    def get(self, key, default=None):
        """
        
        :param key: 
        :param default: 
        :return: 
        """
        return self._data.get(key, default)

    def data(self):
        """
        
        :return: 
        """
        return self._data

    @staticmethod
    def freeze(cls, obj, **_):
        """
        
        :param cls: 
        :param obj: 
        :param _: 
        :return: 
        """
        return cls.recurse(
            obj,
            map_fn=FrozenMap,
            list_fn=tuple
        )

    hashable_types = (
        six.integer_types,
        six.text_type,
        six.binary_type,
        bool,
        float,
        type(None),
        ndarray,
        Enum,
        BuiltinFunctionType,
        six.binary_type,
        FunctionType,
        UUID,
        datetime.datetime,
        datetime.timedelta
    )

    @staticmethod
    def recurse(cls,
                obj,
                map_fn=lambda x: x,
                list_fn=lambda x: x,
                object_fn=lambda x: x):
        """

        :param cls: 
        :param obj: 
        :param map_fn: 
        :param list_fn: 
        :param object_fn: 
        :return: 
        """
        funcs = dict(
            map_fn=map_fn,
            list_fn=list_fn,
            object_fn=object_fn
        )
        obj_type = type(obj)
        if isinstance(obj, Mapping):
            items = six.iteritems(obj)
            map_items = (
                (k, cls.recurse(v, **funcs)) for k, v in items
            )
            new_map = obj_type(map_items)
            new_obj = map_fn(new_map)
        elif cls.is_for_list_fn(obj):
            map_items = (cls.recurse(v, **funcs) for v in obj)
            new_list = obj_type(map_items)
            new_obj = list_fn(new_list)
        elif not isinstance(obj, cls.hashable_types):
            new_obj = object_fn(obj)
        else:
            new_obj = obj
        return new_obj

    @staticmethod
    def is_for_list_fn(obj, **_):
        """
        
        :param obj: 
        :param _: 
        :return: 
        """

        if isinstance(obj, str):
            return False
        if isinstance(obj, Sequence) or isinstance(obj, Set):
            return True
        return False
