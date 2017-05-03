# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .deviation_swfilter import DeviationSWFilter
from .difference_swfilter import DifferenceSWFilter


class DeviationDifferenceSWFilter(DifferenceSWFilter,
                                  DeviationSWFilter):
    """
    Example how to build combined sliding window filters
    """

    __logger = logging.getLogger(__name__)
