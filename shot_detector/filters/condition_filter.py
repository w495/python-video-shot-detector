# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.utils.dsl_kwargs import dsl_kwargs_decorator
from .filter import Filter


class ConditionFilter(Filter):
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

    def conditional_objects(self, objects,
                            condition=None,
                            **kwargs):

        for obj in objects:
            if obj.feature > 0:
                yield obj
