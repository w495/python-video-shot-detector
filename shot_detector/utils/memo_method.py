# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


import functools
import weakref


class MemoMethod(object):

    __slots__ = [
        'lru_args',
        'lru_kwargs',
    ]

    def __init__(self, *lru_args, **lru_kwargs):
        self.lru_args = lru_args
        self.lru_kwargs = lru_kwargs

    def __call__(self, func):

        @functools.wraps(func)
        def wrapped_func(wrapped_self, *wrapped_args, **wrapped_kwargs):
            # We're storing the wrapped method inside the instance.
            # If we had a strong reference
            # to self the instance would never die.
            weak_wrapped_self = weakref.ref(wrapped_self)
            
            @functools.wraps(func)
            @functools.lru_cache(
                *self.lru_args,
                **self.lru_kwargs
            )
            def cached_method(*cached_args, **cached_kwargs):
                retult = func(
                    weak_wrapped_self(),
                    *cached_args,
                    **cached_kwargs
                )
                return retult

            setattr(wrapped_self, func.__name__, cached_method)

            cached_result = cached_method(
                *wrapped_args,
                **wrapped_kwargs
            )
            return cached_result
        return wrapped_func


memo_method = MemoMethod
