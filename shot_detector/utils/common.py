# -*- coding: utf8 -*-

from __future__ import absolute_import

import six
import inspect
import types
import collections


def car(lst):
    return (lst or [None])[0]


def unique(a):
    seen = set()
    return [seen.add(x) or x for x in a if x not in seen]


def is_whole(x):
    if (x % 1 == 0):
        return True
    else:
        return False


def is_instance(obj):
    import inspect, types
    if not hasattr(obj, '__dict__'):
        return False
    if inspect.isroutine(obj):
        return False
    if type(obj) == types.TypeType:  # alternatively inspect.isclass(obj)
        # class type
        return False
    else:
        return True


def get_objdata_dict(obj, ext_classes_keys=[]):
    res = []
    for key, val in inspect.getmembers(
            obj,
            predicate=lambda x: not inspect.isroutine(x)
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
                key = "%s (%s)" % (key, len(rval_list))
                res += [(key, collections.OrderedDict(rval_list))]
            else:
                res += [(key, val)]
    return collections.OrderedDict(res)
