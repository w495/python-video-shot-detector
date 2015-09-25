# -*- coding: utf-8 -*-

import logging
import time
import types

import six


class LogMeta(type):
    """
        Metaclass for logging every call of every method of target class.
    """

    def __new__(mcs, class_name, bases, attr_dict):
        mcs.logger = logging.getLogger(__name__)
        if mcs.logger.isEnabledFor(logging.DEBUG):
            for key, value in six.iteritems(attr_dict):
                if isinstance(value, types.FunctionType):
                    attr_dict[key] = mcs.decorate(class_name, value)
                elif isinstance(value, types.LambdaType):
                    attr_dict[key] = mcs.decorate(class_name, value)
                elif isinstance(value, types.MethodType):
                    attr_dict[key] = mcs.decorate(class_name, value)
                elif isinstance(value, types.FrameType):
                    attr_dict[key] = mcs.decorate(class_name, value)
        return super(LogMeta, mcs).__new__(mcs, class_name, bases, attr_dict)

    @classmethod
    def decorate(mcs, class_name, func):
        """
        Decorate method `func`.
        Every call of `func` will be reported to logger.
        This function (decorate) calls only one time
        — at target class construction,

        :param class_name: string
            the name of target class
        :param func: function | method | lambda | frame
            input method for decoration
        :return: wrapped(func)
            decorated version of input function
        """
        logger = mcs.logger
        func.ncalls = 0

        def wrapper(self, *args, **kwargs):
            func.ncalls += 1
            tm = time.time()
            logger.debug("[%s]   call    %s.%s.%s" % (
                func.ncalls,
                self.__module__,
                class_name,
                func.__name__
            ))
            res = func(self, *args, **kwargs)
            dtm = time.time() - tm
            logger.debug("[%s] (%.5f) %s.%s.%s" % (
                func.ncalls,
                dtm,
                self.__module__,
                class_name,
                func.__name__
            ))
            return res

        return wrapper
