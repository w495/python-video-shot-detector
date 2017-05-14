# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import functools

from .repr_hash import ReprHash


class MemoDict(dict):
    pass


class MemoItemDict(dict):
    pass


class Memo(object):
    global_storage = MemoDict()

    def __init__(self, name=None):
        self.storage = MemoDict()
        self.global_storage.setdefault(name, self.storage)

    def __call__(self, func):
        self.storage.setdefault(func.__name__, MemoItemDict())

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            key = self.make_key(*args, **kwargs)
            storage = self.storage.get(func.__name__)
            value = storage.get(key)
            if value:
                return value
            value = func(*args, **kwargs)
            storage[key] = value
            return value

        return new_func

    def make_key(self, *args, **kwargs):
        repr_hash = ReprHash(
            obj=tuple([args, kwargs])
        )
        return repr_hash


memo = Memo
