# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_queue_process_pool import BaseQueueProcessPool


class SaveStateProcessPool(BaseQueueProcessPool):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    @staticmethod
    def map(func, iterable, *args, **kwargs):
        """
        
        :param func: 
        :param iterable: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        result = None
        for item in iterable:
            result = func(item, prev_result=result, *args, **kwargs)
        return result
