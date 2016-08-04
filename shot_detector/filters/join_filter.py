# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .filter import Filter


class JoinFilter(Filter):
    __logger = logging.getLogger(__name__)

    def __call__(self, a, b, **kwargs):
        return a.join(b)
