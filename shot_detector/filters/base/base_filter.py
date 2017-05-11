# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
from builtins import zip

from shot_detector.utils import LazyHelper, iter


class BaseFilter(LazyHelper):
    """
        Base filter class.

    """
    __logger = logging.getLogger(__name__)

    @classmethod
    def update_kwargs_methods(cls):
        """
        
        :return: 
        """
        return {
            cls.__call__,
            cls.filter_objects,
            cls.filter_features,
            cls.filter_feature_item
        }

    def filter_objects_as_list(self, objects, **kwargs):
        """

        :param objects:
        :param kwargs:
        :return:
        """
        objects = self.filter_objects(objects, **kwargs)
        objects = list(objects)
        return objects

    def filter_objects(self, objects, **kwargs):
        """

        :param objects:
        :param kwargs:
        :return:
        """
        objects = iter.handle_content(
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
        WARNING:    It cannot be static, due to `LazyHelperWrapper`

        :param feature:
        :param _:
        :return:
        """
        return feature
