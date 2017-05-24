# -*- coding: utf8 -*-

"""
    Some compound objects like dict and sliding window
"""

from __future__ import absolute_import, division, print_function

import collections
import inspect


def object_data_dict(obj, ext_classes_keys=None):
    """

    :param obj: 
    :param ext_classes_keys: 
    :return: 
    """
    if ext_classes_keys is None:
        ext_classes_keys = []
    res = []
    for key, val in inspect.getmembers(
            obj,
            predicate=lambda x: not inspect.isroutine(x)
    ):
        if not key.startswith('__'):
            if key in ext_classes_keys:
                try:
                    val_dict = object_data_dict(val, ext_classes_keys)
                    res += [(key, val_dict)]
                except ValueError:
                    res += [(key, str(val))]
            elif type(val) in (tuple, list):
                val_list = list(val)
                rval_list = []
                for i, xval in enumerate(val_list):
                    nval = object_data_dict(xval, ext_classes_keys)
                    rval_list += [(str(i), nval)]
                key = "%s (%s)" % (key, len(rval_list))
                # noinspection PyArgumentList
                res += [(key, collections.OrderedDict(rval_list))]
            else:
                res += [(key, val)]
    # noinspection PyArgumentList
    return collections.OrderedDict(res)
