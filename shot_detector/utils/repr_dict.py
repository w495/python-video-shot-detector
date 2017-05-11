# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import itertools
import json
import logging
import types
from enum import Enum
import six
from types import BuiltinFunctionType, FunctionType

class ReprDict(object):
    """
        ...
    """

    __slots__ = [
        'logger',
        'obj_type',
        'obj'
    ]

    def __init__(self, obj_type=None, obj=None):
        """
        
        :param obj: 
        """
        self.obj_type = obj_type
        self.obj = obj
        self.logger = logging.getLogger(__name__)


    def __repr__(self):
        """

        :return:
        """
        repr_dict = self.object(self.obj)
        return repr_dict

    def __str__(self):
        """

        :return:
        """
        repr_dict = self.object(self.obj)
        repr_json = json.dumps(repr_dict, indent=2)
        return repr_json

    def object(self, obj):
        """

        :param obj: 
        :return: 
        """
        name = self.object_type(obj)
        var_dict = self.object_vars(obj)
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

    def object_vars(self, obj):
        """

        :param obj: 
        :return: 
        """
        tuple_seq = self.object_vars_tuple_seq(obj)
        repr_dict = dict(tuple_seq)
        return repr_dict

    def object_vars_tuple_seq(self, obj):
        """

        :param obj: 
        :return: 
        """
        obj_vars = vars(obj)
        obj_vars_seq = six.iteritems(obj_vars)
        for key, value in obj_vars_seq:
            repr_value = self.item(value)
            yield (key, repr_value)

    def item(self, value):
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
        elif isinstance(value, six.integer_types):
            return value
        elif isinstance(value, six.text_type):
            return value
        elif isinstance(value, six.binary_type):
            return value
        elif isinstance(value, Enum):
            return str(value)
        elif isinstance(value, BuiltinFunctionType):
            return str(value)
        elif isinstance(value, FunctionType):
            return str(value)
        elif isinstance(value, bool):
            return value
        elif isinstance(value, float):
            return value
        elif value is None:
            return None

        self.logger.warning('unknown value = %s', value)
        return str(value)

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
        repr_list = list(repr_seq)
        return repr_list

    def item_seq(self, item_seq):
        """

        :param item_seq: 
        :return: 
        """
        for item in item_seq:
            item = self.item(item)
            yield item
