# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from .base_filter import BaseFilter

import six


class BaseNestedFilter(BaseFilter):

    pass

    # def to_dict_item_obj(self, value):
    #     if isinstance(value, BaseNestedFilter):
    #         return self.to_dict_nested_filter(value)
    #     return super(BaseNestedFilter, self).to_dict_item_obj(value)
    #
    # def to_dict_nested_filter(self, item):
    #     name = type(item).__name__
    #     var_dict = dict(self.filtered_vars(item))
    #     dict_repr = {
    #         name: var_dict
    #     }
    #     return dict_repr

    #
    # def filtered_vars(self, item):
    #     for key, value in six.iteritems(vars(item)):
    #         if key != '_options':
    #             yield (key, value)