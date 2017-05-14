# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.filters.base import BasePlainFilter


#
# from .filter_operator import FilterOperator

class FilterCastFeatures(BasePlainFilter):
    """
        Casts every filtered value to the same type (`cast`-param).

        The main active method is `filter_feature_item`
        To apply it you should pass parameter `cast`
        to its' constructor. cast should be an a callable object
    """

    __logger = logging.getLogger(__name__)

    op_func = None

    def filter_feature_item(self, feature, **kwargs):
        """

        :param feature:
        :param callable cast:
        :return:
        """
        if hasattr(self.op_func, '__call__'):
            # if isinstance(feature, tuple):
            #     print('cast = ', cast)
            #     print ('feature = ', feature)
            feature = self.op_func(feature)
        else:
            feature = self.op_func

        return feature

        # def reduce_with_op_func(self, feature_tuple, **kwargs):
        #     """
        #
        #     :param feature_tuple:
        #     :param kwargs:
        #     :return:
        #     """
        #
        #     op_func_args = self.prepare_op_func_args(feature_tuple)
        #
        #
        #     result = self._reduce_features(op_func_args)
        #
        #     #print('self.result = ', result)
        #
        #     return result
        #
        #
        #
        # def _reduce_features(self, op_func_args, **kwargs):
        #     """
        #
        #     :param features:
        #     :param kwargs:
        #     :return:
        #     """
        #
        #     for features in op_func_args:
        #         for feature in features:
        #             res = self.op_func(feature)
        #             return res
