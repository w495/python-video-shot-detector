# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from .difference_swfilter import DifferenceSWFilter
from .deviation_swfilter import DeviationSWFilter


class DeviationDifferenceSWFilter(DifferenceSWFilter, DeviationSWFilter):
    """
    Example how to build combined sliding window filters
    """

    __logger = logging.getLogger(__name__)

