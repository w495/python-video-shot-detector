# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from .math_filter import MathFilter


class SgnChangeFilter(MathFilter):
    
    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, **kwargs):

        prev = 0
        for feature in features:
            curr = int(feature >= 0)
            if prev != curr:
                yield feature * 0.0 + (prev - curr)
            else:
                yield feature * 0.0
            prev = curr

