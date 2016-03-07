# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import operator as op
import numpy as np

from .filter import Filter

class FilterCastFeatures(Filter):
    """
        Casts every filtered value to the same type (`cast`-param).

        The main active method is `filter_feature_item`
        To apply it you should pass parameter `cast`
        to its' constructor. cast should be an a callable object
    """

    __logger = logging.getLogger(__name__)


    def filter_feature_item(self, feature, cast=Filter, **kwargs):
        feature = cast(feature)
        return feature