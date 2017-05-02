# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from .math_filter import MathFilter


class ExpFilter(MathFilter):
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self,
                            feature,
                            **kwargs):
        return self.exp(feature, **kwargs)
