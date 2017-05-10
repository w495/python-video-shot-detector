# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import itertools
import json
import logging
import types
# PY2 & PY3 — compatibility
from builtins import zip

import six

from shot_detector.utils.iter import handle_content
from shot_detector.utils.log_meta import ignore_log_meta
from .base_filter_wrapper import BaseFilterWrapper


class BaseFilter(six.with_metaclass(BaseFilterWrapper)):
    """
        Base filter class.

    """
    __logger = logging.getLogger(__name__)

    _options = None

    _counter = 0

    class Options(object):
        """
            Initial config for filter-options
        """
        pass

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        BaseFilter._counter += 1
        self._id = BaseFilter._counter
        self._options = kwargs

        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def __call__(self, **kwargs):
        """
        Copy self with replaced `kwargs`.

        Old kwargs, that was not override are also available.

        :param kwargs:
        :return:
        """
        return type(self)(**kwargs)

    def __repr__(self):
        repr = json.dumps(
            self.to_dict(),
            indent=2
        )
        return repr

    def to_dict(self):
        return self.to_dict_item_obj(self)

    def to_dict_item(self, value):
        if isinstance(value, BaseFilter):
            return value.to_dict_item_obj(value)
        if isinstance(value, list):
            return self.to_dict_item_list(value)
        elif isinstance(value, types.GeneratorType):
            value, _ = itertools.tee(value)
            return self.to_dict_item_list(value)
        elif isinstance(value, dict):
            return self.to_dict_item_dict(value)
        elif isinstance(value, six.integer_types):
            return int(value)
        elif isinstance(value, bool):
            return bool(value)
        elif isinstance(value, float):
            return float(value)
        elif value is None:
            return None
        return str(value)

    @staticmethod
    def to_dict_item_obj(item):
        name = type(item).__name__
        var_dict = item.filtered_vars(item)
        return {name: var_dict}

    def filtered_vars(self, item):
        return dict(item.filtered_vars_seq(item))

    @staticmethod
    def filtered_vars_seq(item):
        for key, value in six.iteritems(vars(item)):
            if key != '_options':
                yield (key, item.to_dict_item(value))

    def to_dict_item_dict(self, items):
        return dict(self.to_dict_item_dict_seq(items))

    def to_dict_item_dict_seq(self, items):
        for key, value in six.iteritems(items):
            yield (key, self.to_dict_item(value))

    def to_dict_item_list(self, items):
        return list(self.to_dict_item_list_seq(items))

    def to_dict_item_list_seq(self, items):
        for item in items:
            yield self.to_dict_item(item)

    @ignore_log_meta
    def get(self, attr, default=None):
        """

        :param attr:
        :param default:
        :return:
        """
        if not self._options:
            self._options = dict()
        return self._options.get(attr, default)

    @property
    def default_options(self):
        """
        
        :return: 
        """
        dict_options = dict()
        if hasattr(self, 'Options') and isinstance(self.Options, type):
            dict_options = dict(self.default_options_seq)
        return dict_options

    @property
    def default_options_seq(self):
        """

        :return: 
        """

        for key, value in six.iteritems(vars(self.Options)):
            if not key.startswith('__'):
                yield key, value

    @ignore_log_meta
    def handle_options(self, options):
        """

        :param dict options:
        :return:
        """
        if not self._options:
            self._options = self.default_options
        options = dict(self._options, **options)
        return options

    def filter_objects_as_list(self, objects, **kwargs):
        """

        :param objects:
        :param kwargs:
        :return:
        """
        import os
        self.__logger.debug('start getpid = %s', os.getpid())
        objects = self.filter_objects(objects, **kwargs)
        objects = list(objects)
        self.__logger.debug('stop  getpid = %s', os.getpid())
        return objects

    def filter_objects(self, objects, **kwargs):
        """

        :param objects:
        :param kwargs:
        :return:
        """
        objects = handle_content(
            objects,
            self.object_features,
            self.filter_features,
            self.update_objects,
            **kwargs
        )
        return objects

    @staticmethod
    def object_features(iterable, **_):
        """

        :param iterable:
        :param _:
        :return:
        """
        for obj in iterable:
            if hasattr(obj, 'feature'):
                yield obj.feature

    def update_objects(self, objects, features, **_):
        """

        :param objects:
        :param features:
        :param _:
        :return:
        """
        for obj, feature in zip(objects, features):
            yield self.update_object(
                obj=obj,
                feature=feature
            )

    @staticmethod
    def update_object(obj, feature, **_):
        """
        
        :param obj: 
        :param feature: 
        :param _: 
        :return: 
        """
        #
        # self.__logger.warn('feature  = %s', feature)

        return obj.copy(feature=feature)

    def filter_features(self, features, **kwargs):
        """

        :param features:
        :param kwargs:
        :return:
        """
        for feature in features:
            yield self.filter_feature_item(feature, **kwargs)

    def filter_feature_item(self, feature, **_):
        """
        WARNING:    It cannot be static, due to `BaseFilterWrapper`

        :param feature:
        :param _:
        :return:
        """
        return feature
