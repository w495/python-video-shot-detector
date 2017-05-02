# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from .math_filter import MathFilter


class BoundFilter(MathFilter):
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, **kwargs):
        bound = kwargs.pop('bound', 0)
        offset = kwargs.pop('offset', 0)
        upper_bound = kwargs.pop('upper_bound', offset + bound)
        lower_bound = kwargs.pop('lower_bound', offset - bound)
        if self.bool(feature < lower_bound, **kwargs):
            feature = lower_bound
        elif self.bool(upper_bound < feature, **kwargs):
            feature = upper_bound
        return feature
