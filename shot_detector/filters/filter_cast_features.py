# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function

import logging

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
        """
        
        :param feature: 
        :param cast: 
        :param kwargs: 
        :return: 
        """
        if hasattr(cast, '__call__'):
            feature = cast(feature)
        else:
            feature = cast

        return feature
