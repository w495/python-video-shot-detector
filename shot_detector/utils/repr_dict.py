# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import json
import logging
import datetime
from enum import Enum
from types import BuiltinFunctionType, FunctionType
from uuid import UUID

import six
from numpy import ndarray


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

    def __init__(self, obj_type=None, obj=None, indent=2):
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
        repr_dict = self.object(self.obj)
        return str(repr_dict)

    def __str__(self):
        """

        :return:
        """
        repr_dict = self.object(self.obj)
        repr_json = json.dumps(
            repr_dict,
            indent=self.indent,
            sort_keys=True,
            default=lambda x: self.item(x)
        )
        return repr_json

    def __iter__(self):
        repr_dict = self.object(self.obj)
        return six.iteritems(repr_dict)


    def object(self, obj):
        """

        :param obj: 
        :return: 
        """
        name = self.object_type(obj)
        var_dict = self.object_fields(obj)
        repr_dict = {name: var_dict}
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
        repr_dict = dict(tuple_seq)
        return repr_dict

    def object_field_seq(self, obj):
        """

        :param obj: 
        :return: 
        """
        obj_fields = self.vars_and_slots(obj)
        obj_field_seq = six.iteritems(obj_fields)
        for key, value in obj_field_seq:
            repr_value = self.item(value)
            yield (key, repr_value)

    def vars_and_slots(self, obj):
        """
        
        :param obj: 
        :return: 
        """
        obj_vars = dict()
        obj_slots = dict()
        if hasattr(obj, '__dict__'):
            obj_vars = self.vars(obj)
        if hasattr(obj, '__slots__'):
            obj_slots = self.slots(obj)
        obj_fields = dict(
            obj_vars,
            **obj_slots
        )
        return obj_fields

    def vars(self, obj):
        """
        
        :param obj: 
        :return: 
        """
        obj_vars = vars(obj)
        return obj_vars

    def slots(self, obj):
        """
        
        :param obj: 
        :return: 
        """
        vars_seq = self.slots_seq(obj)
        return dict(vars_seq)

    def slots_seq(self, obj):
        """
        
        :param obj: 
        :return: 
        """
        attrs = self.mro_slots_seq(obj)
        for attr in attrs:
            item = attr, getattr(obj, attr, None)
            yield item

    def mro_slots_seq(self, obj):
        mro = type(obj).mro()
        for cls in mro:
            slots = getattr(cls, '__slots__', list())
            for slot in slots:
                yield slot

    def to_dict(self):
        var_dict = self.object_fields(self.obj)
        return var_dict

    def item(self, value):
        """
        
        :param value: 
        :return: 
        """

        repr_dict = self.external(value)
        if isinstance(repr_dict, ReprDict):
            return repr_dict.raw_item(value)
        elif isinstance(repr_dict, self.external_item_types()):
            return repr_dict
        else:
            return self.raw_item(value)

    def external_item_types(self):
        return (
            dict,
            list,
            tuple,
        )

    def external(self, value):
        repr_dict_attrs = self.repr_dict_attrs()

        for attr in repr_dict_attrs:
            repr_dict_method = getattr(value, attr, None)
            if repr_dict_method:
                repr_dict = repr_dict_method()
                return repr_dict

    def repr_dict_attrs(self):
        return (
            'repr_dict',
        )

    def raw_item(self, value):
        """

        :param value: 
        :return: 
        """
        if isinstance(value, self.obj_type):
            return self.object(value)
        elif isinstance(value, dict):
            return self.item_dict(value)
        elif isinstance(value, list):
            return self.item_list(value)
        elif isinstance(value, self.string_types()):
            return str(value)
        elif isinstance(value, self.as_is_types()):
            return value
        elif isinstance(value, ndarray):
            return value.tolist()
        elif value is None:
            return None
        elif hasattr(value, '__iter__'):
            return dict(value)

        # self.logger.warning('unknown value = %s', value, )

        return str(value)

    def as_is_types(self):
        return (
            six.integer_types,
            six.text_type,
            six.binary_type,
            bool,
            float
        )

    def string_types(self):
        return (
            Enum,
            BuiltinFunctionType,
            six.binary_type,
            FunctionType,
            UUID,
            datetime.datetime,
            datetime.timedelta
        )

    def item_dict(self, item_seq):
        """

        :param item_seq: 
        :return: 
        """
        tuple_seq = self.item_tuple_seq(item_seq)
        repr_dict = dict(tuple_seq)
        return repr_dict

    def item_tuple_seq(self, item_seq):
        """

        :param item_seq: 
        :return: 
        """
        for key, value in six.iteritems(item_seq):
            repr_value = self.item(value)
            yield (key, repr_value)

    def item_list(self, item_seq):
        """

        :param item_seq: 
        :return: 
        """
        repr_seq = self.item_seq(item_seq)
        repr_dict = dict(repr_seq)
        return repr_dict

    def item_seq(self, item_seq):
        """

        :param item_seq: 
        :return: 
        """
        for index, item in enumerate(item_seq):
            item = self.item(item)
            yield index, item
