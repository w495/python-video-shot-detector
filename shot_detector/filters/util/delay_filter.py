# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import itertools
import logging

from shot_detector.filters.dsl import DslPlainFilter


class DelayFilter(DslPlainFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    @DslPlainFilter.kwargs_decorator(
        ('delay', int, 'd', 'l', '__delay'),
    )
    def filter_objects(self, objects, delay=0, **kwargs):
        """
        
        :param objects: 
        :param delay: 
        :param kwargs: 
        :return: 
        """

        it_objects = iter(objects)
        # noinspection PyArgumentEqualDefault
        delayed_objects = itertools.islice(
            it_objects,
            delay,
            None
        )
        return delayed_objects

    def __call__(self, delay=None, **kwargs):
        return super(DelayFilter, self).__call__(
            __delay=delay,
            **kwargs
        )
