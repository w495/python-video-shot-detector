# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import itertools


from shot_detector.utils.dsl_kwargs import dsl_kwargs_decorator

from .filter import Filter


class JoinFilter(Filter):

    __logger = logging.getLogger(__name__)

    def __call__(self, a, b, **kwargs):

        return a.join(b)
