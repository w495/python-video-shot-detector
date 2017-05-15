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
    """
        MemoDict
    """
    pass


class MemoItemDict(dict):
    """
        MemoItemDict
    """
    pass


class Memo(object):
    """
        Memo
    """

    global_storage = MemoDict()

    def __init__(self, name=None):
        """
        
        :param name: 
        """
        self.storage = MemoDict()
        self.global_storage.setdefault(name, self.storage)

    def __call__(self, func):
        """
        
        :param func: 
        :return: 
        """
        self.storage.setdefault(func.__name__, MemoItemDict())

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            """
            
            :param args: 
            :param kwargs: 
            :return: 
            """
            key = self.make_key(*args, **kwargs)
            storage = self.storage.get(func.__name__)
            value = storage.get(key)
            if value:
                return value
            value = func(*args, **kwargs)
            storage[key] = value
            return value

        return new_func

    @staticmethod
    def make_key(*args, **kwargs):
        """
        
        :param args: 
        :param kwargs: 
        :return: 
        """
        repr_hash = ReprHash(
            obj=tuple([args, kwargs])
        )
        return repr_hash


memo = Memo
