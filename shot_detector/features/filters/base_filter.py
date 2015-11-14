# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import copy
from functools import wraps

import itertools
import collections
import logging

from shot_detector.utils.common import save_features_as_image

# from shot_detector.handlers import BasePointHandler

from shot_detector.utils.log_meta import LogMeta


class BaseFilterWrapper(type):
    __logger = logging.getLogger(__name__)
    __update_kwargs_fnames = (
        '__init__',
        '__call__',
        'filter_objects',
        'filter_features',
        'filter_item',
    )
    def __new__(mcs, class_name, bases, attr_dict):
        for fnames in mcs.__update_kwargs_fnames:
            function = attr_dict.get(fnames)
            if function:
                attr_dict[fnames] = mcs.update_kwargs(class_name, function)
        return super(BaseFilterWrapper, mcs).__new__(mcs, class_name, bases, attr_dict)
    @classmethod
    def update_kwargs(mcs, class_name, function):
        def wrapper(self, *args, **kwargs):
            updated_kwargs = self.get_options(**kwargs)
            return function(self, *args, **updated_kwargs)
        return wrapper


class BaseFilter(six.with_metaclass(BaseFilterWrapper)):

    __logger = logging.getLogger(__name__)

    __number_of_calls = None

    options = None
    sequential_filters = None
    parallel_filters = None

    def __init__(self, **kwargs):
        self.options = kwargs
        BaseFilter.__number_of_calls = 0

    def __call__(self, **kwargs):
        BaseFilter.__number_of_calls += 1
        if 1 == BaseFilter.__number_of_calls:
            return self
        return self.__class__(**kwargs)

    def get(self, attr, default=None):
        if not self.options:
            self.options = dict()
        return self.options.get(attr, default)

    def get_options(self, **kwargs):
        if not self.options:
            self.options = dict()
        options = dict(self.options, **kwargs)
        return options

    def filter_objects(self, objects, **kwargs):
        features = self.get_features(objects, **kwargs)
        filtered_features = self.filter_features(features, x=1, **kwargs)
        new_iterable = self.update_objects(objects, filtered_features, **kwargs)
        return new_iterable

    def get_features(self, iterable, **kwargs):
        for item in iterable:
            if hasattr(item, 'feature'):
                yield item.feature

    def update_objects(self, objects, features, **kwargs):
        for obj, feature in itertools.izip(objects, features):
            obj.feature = feature
            yield obj

    def filter_features(self, features, **kwargs):
        for feature in features:
            yield self.filter_item(feature, **kwargs)

    def filter_item(self, feature, **kwargs):
        self.__logger.debug('filter_item: not implemented')
        return feature

