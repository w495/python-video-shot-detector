# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import time
import itertools

import six

from shot_detector.utils import ReprDict

from shot_detector.utils.collections import FrozenDict


class BaseVideoUnit(object):
    """
        ...
    """

    __slots__ = [
        '_id',
    ]

    counter = 0

    def __init__(self, **kwargs):
        """

        :param kwargs_items: 
        :param kwargs: 
        """

        BaseVideoUnit.counter += 1
        self._id = FrozenDict(
            id=BaseVideoUnit.counter,
            time=time.time()
        )

    def copy(self, **kwargs):
        """
        
        :param kwargs: 
        :return: 
        """
        obj_type = type(self)
        obj = self.copy_as(obj_type=obj_type, **kwargs)
        return obj

    def copy_as(self, obj_type, **kwargs):
        """

        :param type obj_type: 
        :return: 
        """

        assert issubclass(obj_type, BaseVideoUnit)

        obj = self._copy_as(obj_type, self, **kwargs)
        return obj

    @staticmethod
    def _copy_as(obj_type, obj, **kwargs):
        """
        
        :param type obj_type: 
        :param BaseVideoUnit obj: 
        :return: 
        """

        assert issubclass(obj_type, BaseVideoUnit)
        assert isinstance(obj, BaseVideoUnit)

        old_attrs = obj.vars_and_slots()
        new_kwargs = FrozenDict(
            old_attrs,
            **kwargs
        )
        obj = obj_type(**new_kwargs.data())
        return obj

    def vars_and_slots(self):
        """

        :return: 
        """
        vars_seq = list()
        slots_seq = list()
        if hasattr(self, '__dict__'):
            vars_seq = self.vars_seq()
        if hasattr(self, '__slots__'):
            slots_seq = self.slots_seq()
        vars_and_slots_seq = itertools.chain(vars_seq, slots_seq)
        obj_fields = FrozenDict(vars_and_slots_seq)
        return obj_fields

    def vars_seq(self):
        """
 
        :return: 
        """
        obj_vars = vars(self)
        return six.iteritems(obj_vars)


    def slots_seq(self):
        """
        
        :return: 
        """
        attrs = self.mro_slots_seq()
        for attr in attrs:
            value = getattr(self, attr, None)
            item = attr, value
            yield item

    def mro_slots_seq(self):
        """
        
        :return: 
        """
        mro = type(self).mro()
        for cls in mro:
            slots = getattr(cls, '__slots__', list())
            for slot in slots:
                yield slot

    def __str__(self):
        """

        :return:
        """
        repr_dict = self.repr_dict()
        return str(repr_dict)


    def repr_dict(self):
        """
        
        :return: 
        """
        repr_dict = ReprDict(type(self), self)
        return repr_dict
