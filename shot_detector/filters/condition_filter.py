# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.utils.dsl_kwargs import dsl_kwargs_decorator
from .filter import Filter


class ConditionFilter(Filter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    @dsl_kwargs_decorator(
        ('delay', int, 'd', 'l', '__delay'),
    )
    def filter_objects(self, objects,
                       **kwargs):
        """

        :param objects:
        :param kwargs:
        :return:
        """

        return self.conditional_objects(objects)

    # noinspection PyUnusedLocal
    @staticmethod
    def conditional_objects(objects,
                            condition=None,
                            **kwargs):
        """
        
        :param objects: 
        :param condition: 
        :param kwargs: 
        :return: 
        """

        for obj in objects:
            if obj.feature > 0:
                yield obj
