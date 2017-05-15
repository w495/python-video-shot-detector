# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime
import itertools
import json
import logging
from collections import Iterable
from enum import Enum
from types import BuiltinFunctionType, FunctionType
from uuid import UUID

from multipledispatch import dispatch
from numpy import ndarray
from six import (
    iteritems,
    text_type,
    binary_type,
    integer_types,
)


from .collections.frozen_dict import FrozenDict

class ReprDict(object):
    """
        ...
    """

    __slots__ = [
        'logger',
        'obj_type',
        'obj',
        'indent',
    ]

    as_is_types = (
        integer_types,
        text_type,
        binary_type,
        bool,
        float,
        type(None)
    )

    string_types = (
        Enum,
        BuiltinFunctionType,
        binary_type,
        FunctionType,
        UUID,
        datetime.datetime,
        datetime.timedelta
    )

    external_item_types = (
        FrozenDict,
        list,
        tuple,
    )

    def __init__(self, obj_type=type(None), obj=None, indent=2):
        """

        :param obj: 
        """
        self.obj_type = obj_type
        self.obj = obj
        self.logger = logging.getLogger(__name__)

        self.indent = indent

    def __repr__(self):
        """

        :return:
        """
        repr_dict = self.item(self.obj)
        return str(repr_dict)

    def __str__(self):
        """

        :return:
        """
        repr_dict = self.object_repr(self.obj)
        repr_json = json.dumps(
            repr_dict,
            indent=self.indent,
            sort_keys=True,
            default=lambda x: self.item(x)
        )
        return repr_json

    def __iter__(self):
        repr_dict = self.item(self.obj)
        return iteritems(repr_dict)

    def object_repr(self, obj):
        """

        :param obj: 
        :return: 
        """
        name = self.object_type(obj)
        var_dict = self.object_fields(obj)
        repr_dict = FrozenDict({name: var_dict})
        return repr_dict

    @staticmethod
    def object_type(item):
        """

        :param item: 
        :return: 
        """
        name = type(item).__name__
        return name

    def object_fields(self, obj):
        """

        :param obj: 
        :return: 
        """
        tuple_seq = self.object_field_seq(obj)
        repr_dict = FrozenDict(tuple_seq)
        return repr_dict

    def object_field_seq(self, obj):
        """

        :param obj: 
        :return: 
        """
        obj_fields = self.vars_and_slots(obj)
        obj_field_seq = iteritems(obj_fields)
        for key, value in obj_field_seq:
            repr_value = self.item(value)
            yield (key, repr_value)

    def vars_and_slots(self, obj):
        """

        :param obj: 
        :return: 
        """
        vars_seq = list()
        slots_seq = list()
        if hasattr(obj, '__dict__'):
            vars_seq = self.vars_seq(obj)
        if hasattr(obj, '__slots__'):
            slots_seq = self.slots_seq(obj)
        vars_and_slots_seq = itertools.chain(vars_seq, slots_seq)
        obj_fields = FrozenDict(vars_and_slots_seq)
        return obj_fields

    @staticmethod
    def vars_seq(obj):
        """

        :param obj: 
        :return: 
        """
        obj_vars = vars(obj)
        return iteritems(obj_vars)

    def slots_seq(self, obj):
        """

        :param obj: 
        :return: 
        """
        attrs = self.mro_slots_seq(obj)
        for attr in attrs:
            item = attr, getattr(obj, attr, None)
            yield item

    @staticmethod
    def mro_slots_seq(obj):
        """
        
        :param obj: 
        :return: 
        """
        mro = type(obj).mro()
        for cls in mro:
            slots = getattr(cls, '__slots__', list())
            for slot in slots:
                yield slot

    def item(self, value):
        """

        :param value: 
        :return: 
        """

        repr_dict = self.external(value)
        if isinstance(repr_dict, ReprDict):
            return repr_dict.raw_item(value)
        elif isinstance(repr_dict, self.external_item_types):
            return repr_dict
        else:
            return self.raw_item(value)

    def external(self, value):
        """
        
        :param value: 
        :return: 
        """
        repr_dict_attrs = self.repr_dict_attrs()
        for attr in repr_dict_attrs:
            repr_dict_method = getattr(value, attr, None)
            if repr_dict_method:
                repr_dict = repr_dict_method()
                return repr_dict

    @staticmethod
    def repr_dict_attrs():
        """
        
        :return: 
        """
        return (
            'repr_dict',
        )

    @dispatch(dict)
    def raw_item(self, value):
        """
        
        :param value: 
        :return: 
        """
        tuple_seq = self.raw_item_seq(value)
        repr_dict = FrozenDict(tuple_seq)
        return repr_dict

    @dispatch(list)
    def raw_item(self, value):
        """
        
        :param value: 
        :return: 
        """
        repr_seq = self.raw_item_seq(value)
        repr_dict = FrozenDict(repr_seq)
        return repr_dict

    @dispatch(as_is_types)
    def raw_item(self, value):
        """
        
        :param value: 
        :return: 
        """
        return value

    @dispatch(string_types)
    def raw_item(self, value):
        """
        
        :param value: 
        :return: 
        """
        return str(value)

    @dispatch(ndarray)
    def raw_item(self, value):
        """
        
        :param value: 
        :return: 
        """
        return value.tolist()

    @dispatch(Iterable)
    def raw_item(self, value):
        """
        
        :param value: 
        :return: 
        """
        return FrozenDict(value)

    @dispatch(object)
    def raw_item(self, value):
        """

        :param value: 
        :return: 
        """
        if isinstance(value, self.obj_type):
            return self.object_repr(value)
        # self.logger.warning('unknown value = %s', value, )
        return str(value)

    @dispatch((dict, FrozenDict))
    def raw_item_seq(self, item_seq):
        """

        :param item_seq: 
        :return: 
        """
        for key, value in iteritems(item_seq):
            repr_value = self.item(value)
            yield key, repr_value

    @dispatch(list)
    def raw_item_seq(self, item_seq):
        """

        :param item_seq: 
        :return: 
        """
        for index, item in enumerate(item_seq):
            item = self.item(item)
            yield index, item
