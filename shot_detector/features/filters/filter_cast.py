# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import operator as op
import numpy as np

from .filter import Filter

class FilterCast(Filter):

    __logger = logging.getLogger(__name__)


    def filter_feature_item(self,
                            feature,
                            value=None,
                            cast=Filter,
                            x=None,
                            **kwargs):

        if value is not None:
            return self.cast_to_filter(feature, value)
        feature = cast(feature)
        return feature

    def cast_to_filter(self, feature, value=None):
        return (feature*0 + value)
