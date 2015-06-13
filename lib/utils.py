# -*- coding: utf8 -*-

from __future__ import absolute_import

import hashlib
import copy
import six

import numpy as np

def car(lst):
    return (lst or [None])[0]

def unique(a):
    seen = set()
    return [seen.add(x) or x for x in a if x not in seen]

class SmartDict(dict):
    def __init__(self, *args, **kwargs):
        if(kwargs):
            kwargs.update(self.__dict__)
            self.__dict__ = kwargs
        super(SmartDict, self).__init__(*args, **kwargs)
    def __setattr__(self, attr, value):
        super(SmartDict, self).__setattr__(attr, value)
        super(SmartDict, self).__setitem__(attr, value)
    def __setitem__(self, attr, value):
        super(SmartDict, self).__setattr__(attr, value)
        super(SmartDict, self).__setitem__(attr, value)
    def __delitem__(self, key):
        super(SmartDict, self).__delitem__(key)
        super(SmartDict, self).__delattr__(key)
    def __delattr__(self, key):
        super(SmartDict, self).__delitem__(key)
        super(SmartDict, self).__delattr__(key)

def is_whole(x):
    if(x%1 == 0):
        return True
    else:
        return False

def shrink(self, data, rows, cols):
    row_sp = data.shape[0] / rows
    col_sp = data.shape[1] / cols
    tmp = np.sum(1.0*data[i::row_sp]/row_sp for i in  xrange(row_sp))
    return np.sum(1.0*tmp[:,i::col_sp]/col_sp for i in xrange(col_sp))

def histogram_intersect(h1, h2):
    res  = []
    for i, j in zip(h1, h2):
        q = min(i, j)
        res += [q]
    return res




