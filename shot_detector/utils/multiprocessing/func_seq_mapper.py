# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import psutil


class FuncSeqMapper(object):
    __logger = logging.getLogger(__name__)

    def __init__(self, caller=None):
        self.caller = caller
        self.name = type(caller).__name__

    def map(self, func_seq, *args, **kwargs):
        futures = self.future_list(func_seq, *args, **kwargs)
        result = self.joined_map_seq(futures)
        return result

    def future_list(self, func_seq, *args, **kwargs):
        futures = self.future_seq(func_seq, *args, **kwargs)
        futures = list(futures)  # !important
        return futures

    def func_wrapper(self, func, *args, **kwargs):
        func_class = type(func.__self__).__name__
        func_name = func.__name__
        self.__logger.debug('%s: [^] %s:%s', self.name, func_class,
                            func_name)
        res = func(*args, **kwargs)
        self.__logger.debug('%s: [$] %s:%s', self.name, func_class,
                            func_name)

        process = psutil.Process(os.getpid())

        self.__logger.info('%s', process.memory_info().rss)

        return res

    def future_seq(self, func_seq, *args, **kwargs):
        func_list = list(func_seq)
        workers = len(func_list)
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for func in func_list:
                future = executor.submit(
                    self.func_wrapper,
                    func,
                    *args,
                    **kwargs
                )
                yield future

    @staticmethod
    def joined_map_seq(futures):
        as_completed(futures)
        for future in futures:
            res = future.result()
            yield res
