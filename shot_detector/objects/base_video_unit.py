# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import itertools
import logging

import six

from .second import Second


class BaseVideoUnit(object):
    __source = None

    __time = None
    __global_number = None

    __UNDEFINED = object()

    __logger = logging.getLogger(__name__)

    def __init__(self, kwargs_items=None, **kwargs):
        if kwargs_items:
            self._stored_attr_seq(kwargs_items)
        else:
            self._stored_attr_dict(kwargs)

    def _stored_attr_dict(self, kwargs):
        kwargs_items = six.iteritems(kwargs)

        return self._stored_attr_seq(kwargs_items)

    def _stored_attr_seq(self, kwargs_items):
        for attr, value in kwargs_items:
            # self.__logger.info("attr, value = %s %s", attr, value)
            setattr(self, attr, value)

    @property
    def time(self):
        if self.__time is None:
            if self.source and self.source.time:
                self.__time = Second(self.source.time)
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    @property
    def hms(self):
        if self.time:
            return self.time.hms()
        return '00:00:00'

    @property
    def minsec(self):
        if self.time:
            return self.time.minsec()
        return 0.0

    @property
    def second(self):
        if self.time:
            return self.time
        return 0.0

    @property
    def minute(self):
        if self.time:
            return self.time.minute()
        return 0.0

    @property
    def global_number(self):
        if self.__global_number is None:
            if self.source:
                self.__global_number = self.source.global_number
        return self.__global_number

    @global_number.setter
    def global_number(self, value):
        self.__global_number = value

    @property
    def number(self):
        return self.global_number

    @number.setter
    def number(self, value):
        self.global_number = value

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        self.__source = value

    @classmethod
    def source_sequence(cls, sequence):
        for unit in sequence:
            yield unit.source

    def copy(self, **kwargs):
        old_attr_seq = six.iteritems(vars(self))
        kwargs_seq = six.iteritems(kwargs)
        new_attr_seq = itertools.chain(old_attr_seq, kwargs_seq)
        obj = type(self)(kwargs_items=new_attr_seq)
        return obj

    def __repr__(self):
        repr_list = []
        mro = self.__class__.mro()
        class_name_list = [klass.__name__ for klass in mro]
        for key, value in six.iteritems(vars(self)):
            for name in class_name_list:
                key = key.replace('_{}__'.format(name), '@')
            repr_list += ["'{k}':{v}".format(k=key, v=value)]
        repr_str = ','.join(repr_list)
        return "{%s}" % repr_str

    def __str__(self):
        class_name = self.__class__.__name__
        return "{class_name} {number} {hms} {time}".format(
            class_name=class_name,
            number=self.number,
            hms=self.hms,
            time=self.time,
        )
