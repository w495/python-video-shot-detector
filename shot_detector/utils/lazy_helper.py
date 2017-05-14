# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
from functools import wraps

import six

from .lazy_helper_wrapper import LazyHelperWrapper
from .repr_dict import ReprDict


class LazyHelperInternalState(object):
    """
        ...
    """

    __init_kwargs = None
    __counter = 0

    NAME = '_LazyHelper__internal_state'

    def __init__(self, **kwargs):
        self.__init_kwargs = dict(**kwargs)

    @property
    def init_kwargs(self):
        """

        :return: 
        """
        return self.__init_kwargs

    @staticmethod
    def get_id():
        """

        :return: 
        """
        LazyHelperInternalState.__counter += 1
        return LazyHelperInternalState.__counter


class LazyHelperReprDict(ReprDict):
    """
        Re
    """

    def object_field_seq(self, obj):
        """

        :param obj: 
        :return: 
        """
        obj_vars = vars(obj)
        obj_vars_seq = six.iteritems(obj_vars)
        for key, value in obj_vars_seq:
            if key != LazyHelperInternalState.NAME:
                repr_value = self.item(value)
                yield (key, repr_value)


class LazyHelper(six.with_metaclass(LazyHelperWrapper)):
    """
        Base Update Kwargs Callable Object with 
        passing `**kwargs` from `__init__`
        to each methods from `update_kwargs_methods`.
        It is very helpful for building lazy objects,
        which initialized in constructor and do work
        in some another methods 
            (for example in `update_kwargs_methods`)

    """
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options
        """
        pass

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        self.__internal_state = LazyHelperInternalState(**kwargs)
        self.id = LazyHelperInternalState.get_id()

        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def __call__(self, **kwargs):
        """
        Copy self with replaced `kwargs`.

        Old kwargs, that was not override are also available.

        :param kwargs:
        :return:
        """
        return type(self)(**kwargs)

    def __str__(self):
        """

        :return: 
        """

        repr_dict = LazyHelperReprDict(LazyHelper, self)
        return str(repr_dict)

    @classmethod
    def update_kwargs_methods(cls):
        """

        :return: 
        """
        return {
            cls.__call__
        }

    @classmethod
    def update_kwargs(cls, func):
        """

        :param _class_name: 
        :param func: 
        :return: 
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            """

            :param self: 
            :param args: 
            :param kwargs: 
            :return: 
            """

            updated_kwargs = self.handle_init_kwargs(kwargs)
            res = func(self, *args, **updated_kwargs)
            return res

        return wrapper

    def handle_init_kwargs(self, kwargs):
        """

        :param dict options:
        :return:
        """

        default_kwargs = dict(
            self.__internal_state.init_kwargs,
            **self.default_init_kwargs
        )
        result_kwargs = dict(
            default_kwargs,
            **kwargs
        )
        return result_kwargs

    @property
    def default_init_kwargs(self):
        """
        
        :return: 
        """
        dict_options = dict(self.default_init_kwargs_seq)
        return dict_options

    @property
    def default_init_kwargs_seq(self):
        """

        :return: 
        """

        for key, value in six.iteritems(vars(self.Options)):
            if not key.startswith('__'):
                yield key, value
