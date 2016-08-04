# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

# PY2 & PY3 — compatibility
from builtins import zip

import logging

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
        self._options = kwargs
        self.__name__ = self.__class__.__name__

    def __call__(self, **kwargs):
        """
        Copy self with replaced `kwargs`.

        Old kwargs, that was not override are also available.

        :param kwargs:
        :return:
        """
        return type(self)(**kwargs)

    def __repr__(self):
        name = type(self).__name__
        return "{}({})".format(name, self._options)

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
        doptions = dict()
        if hasattr(self, 'Options') and isinstance(self.Options, type):
            doptions = {
                key: value
                for key, value
                in six.iteritems(vars(self.Options))
                if not key.startswith('__')
                }
        return doptions

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

    def object_features(self, iterable, **_):
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

    def update_object(self, obj, feature, **_):
        """

        :param objects:
        :param features:
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
