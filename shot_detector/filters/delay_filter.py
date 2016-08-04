# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import itertools
import logging

from shot_detector.utils.dsl_kwargs import dsl_kwargs_decorator
from .filter import Filter


class DelayFilter(Filter):
    __logger = logging.getLogger(__name__)

    @dsl_kwargs_decorator(
        ('delay', int, 'd', 'l', '__delay'),
    )
    def filter_objects(self, objects, delay=0, **kwargs):
        """

        :param objects:
        :param kwargs:
        :return:
        """

        it_objects = iter(objects)
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
