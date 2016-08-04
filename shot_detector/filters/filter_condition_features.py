# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .filter import Filter


class FilterConditionFeatures(Filter):
    """
        Casts every filtered value to the same type (`cast`-param).

        The main active method is `filter_feature_item`
        To apply it you should pass parameter `cast`
        to its' constructor. cast should be an a callable object
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self, features, condition=None, **kwargs):
        """

        :param features:
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
                            **kwargs):
        if condition and condition(feature):
            feature = apply(feature)
        return feature

    def _apply_filter_operator(self,
                               first,
                               second,
                               operator=None,
                               *args, **kwargs):

        if first is False:
            return second
