# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function



from .filter_operator import FilterOperator



class FilterTuple(FilterOperator):
    """
        ...
    """


    def reduce_with_op_func(self, feature_tuple, **kwargs):
        """

        :param feature_tuple: 
        :param kwargs: 
        :return: 
        """

        op_func_args = self.prepare_op_func_args(feature_tuple)
        result = tuple(op_func_args)
        return result
