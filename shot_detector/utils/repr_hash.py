# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime
import json
import logging
from collections import Iterable
from enum import Enum
from types import BuiltinFunctionType, FunctionType
from uuid import UUID

from multipledispatch import dispatch
from numpy import ndarray
from six import (
    text_type,
    binary_type,
    integer_types,
)


from .repr_dict import ReprDict

class ReprHash(ReprDict):
    """
        ...
    """

    __slots__ = [
        'logger',
        'obj_type',
        'obj',
        'indent',
    ]

    hashable_types = (
        integer_types,
        text_type,
        binary_type,
        bool,
        float,
        type(None),
        ndarray,
        Enum,
        BuiltinFunctionType,
        binary_type,
        FunctionType,
        UUID,
        datetime.datetime,
        datetime.timedelta
    )

    def to_hashable(self):
        repr_hash = self.item(self.obj)
        return repr_hash

    def object_repr(self, obj):
        """

        :param obj: 
        :return: 
        """
        var_dict = self.object_fields(obj)
        repr_tuple = tuple(var_dict)
        return repr_tuple

    def object_fields(self, obj):
        """

        :param obj: 
        :return: 
        """
        tuple_seq = self.object_field_seq(obj)
        repr_tuple = tuple(tuple_seq)
        return repr_tuple

    @dispatch(dict)
    def raw_item(self, value):
        tuple_seq = self.raw_item_seq(value)
        repr_tuple = tuple(tuple_seq)
        return repr_tuple

    @dispatch(list)
    def raw_item(self, value):
        repr_seq = self.raw_item_seq(value)
        repr_tuple = tuple(repr_seq)
        return repr_tuple

    @dispatch(hashable_types)
    def raw_item(self, value):
        return value

    @dispatch(Iterable)
    def raw_item(self, value):
        return tuple(value)

