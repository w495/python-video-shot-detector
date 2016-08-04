# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import six


# noinspection PyPep8
class ObjDict(object):
    """
        Object that implements `dict` behavior.
        You can see it with example below:
        >>> s = ObjDict(a=1, b=2)

        >>> s
        {'a': 1, 'b': 2}

        >>> s.a
        1
        >>> s.b
        2
        >>> s.a = 3
        >>> s.b = 4
        >>> s
        {'a': 3, 'b': 4}
        >>> s.a
        3
        >>> s.b
        4
        >>> s['a']
        3
        >>> s['b']
        4
        >>> del s.a
        >>> s
        {'b': 4}
        >>> del s['b']
        >>> s
        {}
        >>> s.x = 1
        >>> s
        {'x': 1}
        >>> s['y'] = 10
        >>> s
        {'y': 10, 'x': 1}
        >>>
    """
    __marker__ = object()

    def __init__(self, arg=None, __internal_class__=OrderedDict,
                 **kwargs):
        i_cls = __internal_class__
        self.__internal_dict__ = i_cls()
        for key, value in six.iteritems(i_cls(vars(self.__class__))):
            if not self.__is_internal__(key):
                self.__internal_dict__.update(i_cls({key: value}))
        if arg is not None:
            self.__internal_dict__.update(i_cls(arg))
        self.__internal_dict__.update(i_cls(kwargs))

        for key in dir(self):
            if not self.__is_internal__(
                key) and key in self.__internal_dict__:
                setattr(self, key, self.__internal_dict__.get(key))

    @staticmethod
    def __is_internal__(key):
        if key.startswith('__'):
            return True
        return False

    # noinspection PyUnusedLocal
    def __getitem__(self, attr, **_kwargs):
        res = self.__internal_dict__.get(attr, self.__marker__)
        if res is self.__marker__:
            raise KeyError(attr)
        return res

    # noinspection PyUnusedLocal
    def __getattr__(self, attr, **_kwargs):
        if hasattr(self.__internal_dict__, attr):
            return getattr(self.__internal_dict__, attr)
        if not self.__is_internal__(attr):
            return self.__getitem__(attr)
        raise AttributeError(attr)

    def __setitem__(self, key, value,
                    dict_setitem=OrderedDict.__setitem__):
        return dict_setitem(self.__internal_dict__, key, value)

    def __setattr__(self, key, value):
        if not self.__is_internal__(key):
            self.__setitem__(key, value)
        return super(ObjDict, self).__setattr__(key, value)

    def __delitem__(self, key, dict_delitem=OrderedDict.__delitem__):
        return dict_delitem(self.__internal_dict__, key)

    def __delattr__(self, key):
        if not self.__is_internal__(key):
            return self.__delitem__(key)
        return super(ObjDict, self).__delattr__(key)

    def __iter__(self):
        return OrderedDict.__iter__(self.__internal_dict__)

    def __repr__(self, *args, **kwargs):
        if not self:
            return '%s_%x()' % (self.__class__.__name__, id(self))
        return '%s_%x(%r)' % (
        self.__class__.__name__, id(self), self.__internal_dict__)
