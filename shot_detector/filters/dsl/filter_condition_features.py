# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.filters.base.base_plain_filter import BasePlainFilter


class FilterConditionFeatures(BasePlainFilter):
    """
        Casts every filtered value to the same type (`cast`-param).

        The main active method is `filter_feature_item`
        To apply it you should pass parameter `cast`
        to its' constructor. cast should be an a callable object
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self,
                        features,
                        condition=None,
                        apply=None,
                        **kwargs):
        """
        
        :param features: 
        :param condition: 
        :param apply: 
        :param kwargs: 
        :return: 
        """

        for feature in features:
            if condition and condition(feature):
                yield apply(feature)
            yield feature

    def filter_feature_item(self,
                            feature,
                            condition=None,
                            apply=None,
                            **_):
        """
        
        :param feature: 
        :param condition: 
        :param apply: 
        :return: 
        """
        if condition and condition(feature):
            feature = apply(feature)
        return feature

    # noinspection PyUnusedLocal
    @staticmethod
    def _apply_filter_operator(first,
                               second,
                               operator=None,
                               **_):

        if first is False:
            return second
