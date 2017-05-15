# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import time

import six

from shot_detector.utils import ReprDict


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
        self._id = dict(
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
        new_kwargs = dict(
            old_attrs,
            **kwargs
        )
        obj = obj_type(**new_kwargs)
        return obj

    def vars_and_slots(self):
        """

        :return: 
        """
        obj_vars = dict()
        obj_slots = dict()
        if hasattr(self, '__dict__'):
            obj_vars = self.vars()
        if hasattr(self, '__slots__'):
            obj_slots = self.slots()
        obj_fields = dict(
            obj_vars,
            **obj_slots
        )
        return obj_fields

    def vars(self):
        """
 
        :return: 
        """
        obj_vars = vars(self)
        return obj_vars

    def slots(self):
        """

        :return: 
        """
        vars_seq = self.slots_seq()
        return dict(vars_seq)

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
        mro = type(self).mro()
        for cls in mro:
            slots = getattr(cls, '__slots__', list())
            for slot in slots:
                yield slot

    def __repr__(self):
        """

        :return:
        """
        repr_dict = self.repr_dict()
        return str(repr_dict)

    def __iter__(self):
        repr_dict = self.repr_dict()
        repr_ = dict(repr_dict)
        return six.iteritems(repr_)

    def repr_dict(self):
        repr_dict = ReprDict(type(self), self)
        return repr_dict
