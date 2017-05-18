# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import six

class ObjDictException(Exception):
    pass


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

    def __init__(self,
                 arg=None,
                 _map_class=OrderedDict,
                 **kwargs):

        _map = _map_class()
        _map_keys =  dir(_map)
        _obj_keys = dir(object)
        _bad_keys = _map_keys + _obj_keys + ['_map']
        super().__setattr__('_bad_keys', _bad_keys)
        self_type = type(self)
        self_type_vars = vars(self_type)
        for key, value in six.iteritems(self_type_vars):
            if key not in _bad_keys:
                _map[key] = value
        if arg is not None:
            _map.update(arg)
        _map.update(kwargs)
        super().__setattr__('_map', _map)

    def __getattr__(self, attr, **_):
        sentinel = object()
        res = self._map.get(attr, sentinel)
        if res is sentinel:
            raise AttributeError(attr)
        return res

    def __getitem__(self, attr, **_):
        sentinel = object()
        res = self._map.get(attr, sentinel)
        if res is sentinel:
            raise KeyError(attr)
        return res

    def __setattr__(self,
                    key,
                    value,
                    dict_setitem=OrderedDict.__setitem__):
        if key in self._bad_keys:
            raise ObjDictException('you cannot change internal keys')
        dict_setitem(self._map, key, value)
        return super(ObjDict, self).__setattr__(key, value)

    def __setitem__(self, *args, **kwargs):
        return self.__setattr__(*args, **kwargs)

    def __delattr__(self,
                    key,
                    dict_delitem=OrderedDict.__delitem__):
        dict_delitem(self._map, key)
        return super(ObjDict, self).__delattr__(key)

    def __delitem__(self, *args, **kwargs):
        return self.__delattr__(*args, **kwargs)

    def __iter__(self):
        return OrderedDict.__iter__(self._map)

    def __repr__(self):
        return '{n}({m!r})'.format(n=type(self).__name__, m=self._map)

    def pop(self, *args, **kwargs):
        return self._map.pop(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._map.get(*args, **kwargs)