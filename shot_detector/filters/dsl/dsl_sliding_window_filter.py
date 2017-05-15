# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import itertools
import logging


from shot_detector.utils.iter import handle_content

from shot_detector.filters.base import BaseSlidingWindowFilter

from .dsl_filter_mixin import DslFilterMixin


class DslSlidingWindowFilter(BaseSlidingWindowFilter, DslFilterMixin):
    """
        Basic sliding window filter.
    """

    __logger = logging.getLogger(__name__)

    @DslFilterMixin.dsl_kwargs_decorator(
        ('strict_windows', bool, 'w', 'st', 'sw' 'strict'),
        ('yield_tail', bool, 'y', 'yt'),
        ('centre_samples', bool, 'c', 'cs'),
        ('repeat_windows', bool, 'r', 'rw', 'repeat'),
        ('window_size', int, 's', 'ws', 'size', 'l', 'length'),
        ('overlap_size', int, 'o', 'os' 'overlap'),
        ('repeat_size', int, 'r', 'rs', 'repeat'),
    )
    def filter_windows(self, objects, **kwargs):
        """
        
        :param objects: 
        :param kwargs: 
        :return: 
        """

        objects = super(DslSlidingWindowFilter, self).filter_windows(
            objects,
            **kwargs
        )
        return objects
