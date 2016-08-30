# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
import time
import types
from functools import wraps, partial

import six

from shot_detector.utils.log_settings import configure

configure()


class LogMeta(type):
    """
        Metaclass for logging every call of every method of target class.
    """

    __logger = logging.getLogger(__name__)

    __level = logging.DEBUG

    @staticmethod
    def ignore_method_call(function):
        function.ignore_log_meta = True
        return function

    @staticmethod
    def should_be_overloaded(function):
        function.should_be_overloaded = True
        return function

    @classmethod
    def log_method_call(mcs, function):
        return mcs.decorate(logging.INFO, str(), function)

    @classmethod
    def log_method_call_with(mcs, level):
        def log_method_call(function):
            return mcs.decorate(level, str(), function)

        return log_method_call

    @classmethod
    def log_dummy_call(mcs, function):
        function = mcs.should_be_overloaded(function)
        return mcs.decorate(str(), function)

    def __new__(mcs, class_name, bases, attr_dict):
        if mcs.__logger.isEnabledFor(logging.ERROR):
            for key, value in six.iteritems(attr_dict):
                if (isinstance(value, types.FunctionType) or
                        isinstance(value, types.LambdaType) or
                        isinstance(value, types.MethodType)):
                    attr_dict[key] = mcs.decorate(
                        mcs.__level, class_name, value)

        return super(LogMeta, mcs).__new__(mcs, class_name, bases,
                                           attr_dict)

    @classmethod
    def decorate(mcs, level, class_name, function):
        """
        Decorate method `function`.
        Every call of `function` will be reported to logger.
        This function (decorate) calls only one time
        — at target class construction,

        :param class_name: string
            the name of target class
        :param function: function | method | lambda | frame
            input method for decoration
        :return: wrapped(function)
            decorated version of input function
        """

        if hasattr(function, 'ignore_log_meta'):
            return function

        if hasattr(function, 'should_be_overloaded'):
            pre_call = partial(mcs.dummy_pre_call, level, class_name,
                               function)

            @wraps(function)
            def dummy_wrapper(self, *args, **kwargs):
                pre_call()
                res = function(self, *args, **kwargs)
                return res

            return dummy_wrapper

        pre_call = partial(mcs.pre_call, level, class_name, function)
        post_call = partial(mcs.post_call, level, class_name, function)

        @wraps(function)
        def call_wrapper(self, *args, **kwargs):
            pre_call()
            res = function(self, *args, **kwargs)
            post_call()
            return res

        return call_wrapper

    @classmethod
    def pre_call(mcs, level, class_name, function):
        function = mcs.add_pre_call_attrs(function)
        mcs.__logger.log(level,
                         "[{num}] {mod}.{cls} {fun}".format(
                             num=function.call_number,
                             mod=function.__module__,
                             cls=class_name,
                             fun=function.__name__,
                         ))
        return function

    @classmethod
    def post_call(mcs, level, class_name, function):
        function = mcs.add_post_call_attrs(function)
        mcs.__logger.log(level,
                         "[{num}] {mod}.{cls} {fun} ({time:f})".format(
                             num=function.call_number,
                             mod=function.__module__,
                             cls=class_name,
                             fun=function.__name__,
                             time=function.delta_time,
                         ))
        return function

    @classmethod
    def dummy_pre_call(mcs, level, class_name, function):
        mcs.__logger.log(level,
                         "{mod}.{cls}{fun}: "
                         "dummy method: "
                         "should be overloaded".format(
                             mod=function.__module__,
                             cls=class_name,
                             fun=function.__name__,
                         ))
        return function

    @classmethod
    def add_pre_call_attrs(mcs, function):
        if not hasattr(function, 'call_number'):
            function.call_number = 0
        function.call_number += 1
        function.start_time = time.time()
        return function

    @classmethod
    def add_post_call_attrs(mcs, function):
        function.stop_time = time.time()
        function.delta_time = function.stop_time - function.start_time
        return function


ignore_log_meta = LogMeta.ignore_method_call

log_method_call = LogMeta.log_method_call

log_method_call_with = LogMeta.log_method_call_with

log_dummy_call = LogMeta.log_dummy_call

should_be_overloaded = LogMeta.should_be_overloaded

# for_overload = LogMeta.should_be_overloaded
# overload_me = should_be_overloaded
