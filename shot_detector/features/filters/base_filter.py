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

from shot_detector.utils.log_meta import LogMeta, should_be_overloaded, ignore_log_meta




class BaseFilterWrapper(LogMeta):
    __logger = logging.getLogger(__name__)
    __update_kwargs_fnames = (
        '__init__',
        '__call__',
        'filter_objects',
        'filter_features',
        'filter_feature_item',
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


    options = None

    def __init__(self, **kwargs):
        self.options = kwargs

    def __call__(self, **kwargs):
        return self.__class__(**kwargs)

    @ignore_log_meta
    def get(self, attr, default=None):
        if not self.options:
            self.options = dict()
        return self.options.get(attr, default)

    @ignore_log_meta
    def get_options(self, **kwargs):
        if not self.options:
            self.options = dict()
        options = dict(self.options, **kwargs)
        return options

    def filter_objects(self, objects, **kwargs):
        # Do not forget do this.
        # Otherwice you will handle only odd frames.
        objects, orig_objects = itertools.tee(objects)
        features = self.get_features(objects, **kwargs)
        filtered_features = self.filter_features(features, **kwargs)
        new_iterable = self.update_objects(orig_objects, filtered_features, **kwargs)
        return new_iterable

    @staticmethod
    def get_features(iterable, **kwargs):
        for item in iterable:
            if hasattr(item, 'feature'):
                yield item.feature

    def update_objects(self, objects, features, **kwargs):
        for obj, feature in itertools.izip(objects, features):
            obj.feature = feature
            yield obj

    def filter_features(self, features, **kwargs):
        for feature in features:
            yield self.filter_feature_item(feature, **kwargs)

    @should_be_overloaded
    def filter_feature_item(self, feature, **kwargs):
        return feature

    def sequential(self, other):
        from .base_nested_filter import BaseNestedFilter

        return BaseNestedFilter(
            sequential_filters = [
                self, other
            ]
        )

    def difference(self, other):
        from .filter_difference import FilterDifference

        return FilterDifference(
            parallel_filters = [
                self, other
            ]
        )


    def __sub__(self, other):
        return self.difference(other)

    def __or__(self, other):
        return self.sequential(other)
