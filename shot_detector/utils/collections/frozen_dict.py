# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

import collections

from .frozen_map import FrozenMap

class FrozenDict(FrozenMap):

    def get(self, key, default=None):
        return self._data.get(key, default)

    def data(self):
        return self._data

    @staticmethod
    def recurse(cls, x, map_fn=lambda x: x, list_fn=lambda x: x, object_fn=lambda x: x):
        kwargs = dict(
            map_fn=map_fn,
            list_fn=list_fn,
            object_fn=object_fn
        )
        klass = type(x)
        if isinstance(x, collections.Mapping):
            new_x = map_fn(klass((k, cls.recurse(v, **kwargs)) for k,v in x.items()))
        elif not isinstance(x, str) and (isinstance(x, collections.Sequence) or isinstance(x, collections.Set)):
            new_x = list_fn(klass(cls.recurse(v, **kwargs) for v in x))
        elif not isinstance(x, (int, float, str, bool)):
            new_x = object_fn(x)
        else:
            new_x = x
        return new_x

    def freeze(cls, x, **_):
        return cls.recurse(x, map_fn=FrozenMap, list_fn=tuple)
