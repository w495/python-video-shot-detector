# -*- coding: utf8 -*-

from __future__ import absolute_import

import six

class SmartDict(dict):
    '''
        Object that implements `dict` behavior.
        You can see it with example below:
        
            >> s =  SmartDict(a = 1, b = 2)
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
    '''
    def __init__(self, dict_ = None, *args, **kwargs):
        internal_state = {}

        internal_state.update({
            key: value
            for key, value in six.iteritems(vars(self.__class__))
                if not key.startswith('__')
        })
        internal_state.update(kwargs)
        if None == dict_:
            dict_ = {}
        super(SmartDict, self).__init__(dict_, *args, **internal_state)

    def __getattr__(self, attr):
        return self.get(attr)
    def __delattr__(self, key):
        super(SmartDict, self).__delitem__(key)
    def __setattr__(self, attr, value):
        super(SmartDict, self).__setattr__(attr, value)
        super(SmartDict, self).__setitem__(attr, value)
    def __setitem__(self, attr, value):
        super(SmartDict, self).__setattr__(attr, value)
        super(SmartDict, self).__setitem__(attr, value)


