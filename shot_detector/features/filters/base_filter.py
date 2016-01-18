# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import itertools
import logging

import six

from functools import wraps, partial

# from shot_detector.handlers import BasePointHandler

from shot_detector.utils.log_meta import LogMeta, should_be_overloaded, ignore_log_meta

from shot_detector.utils.iter import handle_content


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
                attr_dict[func_name] = mcs.update_kwargs(class_name, function)
        return super(BaseFilterWrapper, mcs).__new__(mcs, class_name, bases, attr_dict)

    # noinspection PyUnusedLocal
    @classmethod
    def update_kwargs(mcs, _class_name, function):

        @wraps(function)
        def wrapper(self, *args, **kwargs):
            updated_kwargs = self.get_options(**kwargs)
            res = function(self, *args, **updated_kwargs)
            return res
        return wrapper


class BaseFilter(six.with_metaclass(BaseFilterWrapper)):
    __logger = logging.getLogger(__name__)

    options = None

    def __init__(self, **kwargs):
        self.options = kwargs

    def __call__(self, **kwargs):
        return type(self)(**kwargs)

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
        objects = handle_content(
            objects,
            self.get_features,
            self.filter_features,
            self.update_objects,
            **kwargs
        )
        return objects

    # noinspection PyUnusedLocal
    @staticmethod
    def get_features(iterable, **_kwargs):
        for item in iterable:
            if hasattr(item, 'feature'):
                yield item.feature

    # noinspection PyUnusedLocal
    @staticmethod
    def update_objects(objects, features, **_kwargs):
        for obj, feature in itertools.izip(objects, features):
            yield obj.copy(feature=feature)

    def filter_features(self, features, **kwargs):
        for feature in features:
            yield self.filter_feature_item(feature, **kwargs)

    @should_be_overloaded
    def filter_feature_item(self, feature, **kwargs):
        return feature

    def sequential(self, other):
        from .base_nested_filter import BaseNestedFilter

        return BaseNestedFilter(
            sequential_filters=[
                self, other
            ]
        )

    def difference(self, other):
        """
        :param BaseFilter other:
        :return:
        """
        from .filter_difference import FilterDifference

        return FilterDifference(
            parallel_filters=[self, other]
        )

    def __sub__(self, other):
        """
        :param BaseFilter other:
        :return:
        """
        return self.difference(other)

    def __or__(self, other):
        """
        :param BaseFilter other:
        :return:
        """
        return self.sequential(other)
