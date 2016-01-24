# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import itertools
import logging

import six

from shot_detector.utils.iter import handle_content
from shot_detector.utils.log_meta import ignore_log_meta
from .base_filter_wrapper import BaseFilterWrapper


class BaseFilter(six.with_metaclass(BaseFilterWrapper)):
    __logger = logging.getLogger(__name__)

    options = None

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.options = kwargs

    def __call__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return type(self)(**kwargs)

    @ignore_log_meta
    def get(self, attr, default=None):
        """

        :param attr:
        :param default:
        :return:
        """
        if not self.options:
            self.options = dict()
        return self.options.get(attr, default)

    @ignore_log_meta
    def get_options(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        if not self.options:
            self.options = dict()
        options = dict(self.options, **kwargs)
        return options

    def filter_objects(self, objects, **kwargs):
        """

        :param objects:
        :param kwargs:
        :return:
        """
        objects = handle_content(
            objects,
            self.get_features,
            self.filter_features,
            self.update_objects,
            **kwargs
        )
        return objects

    @staticmethod
    def get_features(iterable, **_):
        """

        :param iterable:
        :param _:
        :return:
        """
        for item in iterable:
            if hasattr(item, 'feature'):
                yield item.feature

    @staticmethod
    def update_objects(objects, features, **_):
        """

        :param objects:
        :param features:
        :param _:
        :return:
        """
        for obj, feature in itertools.izip(objects, features):
            yield obj.copy(feature=feature)

    def filter_features(self, features, **kwargs):
        """

        :param features:
        :param kwargs:
        :return:
        """
        for feature in features:
            yield self.filter_feature_item(feature, **kwargs)

    @staticmethod
    def filter_feature_item(feature, **_):
        return feature
