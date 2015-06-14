# -*- coding: utf8 -*-

from __future__ import absolute_import

import datetime
import hashlib
import copy
import six
import inspect
import types
import collections

import numpy as np

def car(lst):
    return (lst or [None])[0]

def unique(a):
    seen = set()
    return [seen.add(x) or x for x in a if x not in seen]


class TimeState(float):
    def time(self):
        return str(datetime.timedelta(seconds=self))


class SmartDict(dict):
    '''
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



def is_whole(x):
    if(x%1 == 0):
        return True
    else:
        return False

def shrink(data, rows, cols):
    width = data.shape[0]
    height = data.shape[1]

    row_sp = width / rows
    col_sp = height / cols

    if(1 == row_sp == col_sp):
        return data

    tmp = np.sum(1.0*data[i::row_sp]/row_sp for i in  xrange(row_sp))
    return np.sum(1.0*tmp[:,i::col_sp]/col_sp for i in xrange(col_sp))

def histogram_intersect(h1, h2):
    res  = []
    for i, j in zip(h1, h2):
        q = min(i, j)
        res += [q]
    return res



def is_instance(obj):
    import inspect, types
    if not hasattr(obj, '__dict__'):
        return False
    if inspect.isroutine(obj):
        return False
    if type(obj) == types.TypeType: # alternatively inspect.isclass(obj)
        # class type
        return False
    else:
        return True


def get_objdata_dict(obj, ext_classes_keys = []):
    res = []
    for key, val in inspect.getmembers(
        obj,
        predicate = lambda x: not inspect.isroutine(x)
    ):
        if (not key.startswith('__')):
            if (key in ext_classes_keys):
                try:
                    val_dict = get_objdata_dict(val, ext_classes_keys)
                    res += [(key, val_dict)]
                except ValueError:
                    res += [(key, str(val))]
            elif (type(val) in (tuple, list)):
                val_list = list(val)
                rval_list = []
                for i, val in enumerate(val_list):
                    nval = get_objdata_dict(val, ext_classes_keys)
                    rval_list += [(str(i), nval)]
                key = "%s (%s)"%(key, len(rval_list))
                res += [(key, collections.OrderedDict(rval_list))]
            else:
                res += [(key, val)]

    return collections.OrderedDict(res)

