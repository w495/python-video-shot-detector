# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six


# noinspection PyPep8
class SmartDict(dict):
    """
        Simple object that implements `dict` behavior.
        You can see it with example below:
        >>> s = SmartDict(a=1, b=2)
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

    def __init__(self, arg=None, __internal_class__=dict, **kwargs):
        i_cls = __internal_class__
        self.__dict__ = i_cls()
        self.__dict__.update(i_cls([(key, value) for key, value in
                                    six.iteritems(vars(self.__class__))
                                    if not key.startswith('__')]))
        if arg is not None:
            self.__dict__.update(i_cls(arg))
        self.__dict__.update(i_cls(kwargs))
        super(SmartDict, self).__init__(**self.__dict__)

    @staticmethod
    def __is_internal__(key):
        if key.startswith('__'):
            return True
        return False

    def __getattr__(self, attr):
        res = self.get(attr, self.__marker__)
        if res is self.__marker__:
            raise AttributeError(attr)
        return res

    def __delattr__(self, key):
        super(SmartDict, self).__delitem__(key)

    def __setattr__(self, attr, value):
        super(SmartDict, self).__setattr__(attr, value)
        if not six.u(attr).startswith('__'):
            super(SmartDict, self).__setitem__(attr, value)

    def __setitem__(self, attr, value):
        if isinstance(attr, str) or isinstance(attr, six.text_type):
            try:
                super(SmartDict, self).__setattr__(attr, value)
            except AttributeError:
                raise AttributeError(attr)

        if not six.u(attr).startswith('__'):
            super(SmartDict, self).__setitem__(attr, value)

    def __repr__(self, *args, **kwargs):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s_%x(%r)' % (
        self.__class__.__name__, id(self), dict(self.__dict__))
