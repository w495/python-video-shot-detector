# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from shot_detector.features.norms import L2Norm
from shot_detector.features.norms import L1Norm


from shot_detector.utils.dsl_kwargs import dsl_kwargs_decorator

from .filter import Filter


class NormFilter(Filter):
    __logger = logging.getLogger(__name__)

    @dsl_kwargs_decorator(
        ('norm_function', bool,
         ['l', 'nm', 'norm', 'f', 'fun', 'function']),
    )
    def filter_feature_item(self,
                            feature,
                            norm_function=None,
                            **kwargs):

        if norm_function is None:
            norm_function = L1Norm.length

        if 1 == norm_function or 'l1' == norm_function:
            norm_function = L1Norm.length
        if 2 == norm_function or 'l2' == norm_function :
            norm_function = L2Norm.length


        return norm_function(feature, **kwargs)
