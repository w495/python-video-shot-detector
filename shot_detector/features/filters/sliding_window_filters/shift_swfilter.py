# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

import numpy as np

from .base_swfilter import BaseSWFilter


class ShiftSWFilter(BaseSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, window_features, **kwargs):
        return window_features[0]
