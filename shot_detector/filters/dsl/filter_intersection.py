# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.filters.base import BaseNestedParallelFilter


class FilterIntersection(BaseNestedParallelFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)
