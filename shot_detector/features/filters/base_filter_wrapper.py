# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
from functools import wraps

from shot_detector.utils.log_meta import LogMeta


class BaseFilterWrapper(LogMeta):
    __logger = logging.getLogger(__name__)
    __update_kwargs_func_name = (
        '__init__',
        '__call__',
        'filter_objects',
        'filter_features',
        'filter_feature_item',
    )

    def __new__(mcs, class_name, bases, attr_dict):
        for func_name in mcs.__update_kwargs_func_name:
            function = attr_dict.get(func_name)
            if function:
                attr_dict[func_name] = mcs.update_kwargs(class_name,
                                                         function)
        return super(BaseFilterWrapper, mcs).__new__(mcs, class_name,
                                                     bases, attr_dict)

    # noinspection PyUnusedLocal
    @classmethod
    def update_kwargs(mcs, _class_name, function):

        @wraps(function)
        def wrapper(self, *args, **kwargs):
            updated_kwargs = self.get_options(**kwargs)
            res = function(self, *args, **updated_kwargs)
            return res

        return wrapper
