# -*- coding: utf-8 -*-

import os
import sys
import logging
import platform
import types
import six
import time

class LogMeta(type):

    def __new__(cls, name, bases, attrs):

        for attr_name, attr_value in six.iteritems(attrs):
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = cls.deco(name, attr_value)
            elif isinstance(attr_value, types.LambdaType):
                attrs[attr_name] = cls.deco(name, attr_value)
            elif isinstance(attr_value, types.MethodType):
                attrs[attr_name] = cls.deco(name, attr_value)
            elif isinstance(attr_value, types.FrameType):
                attrs[attr_name] = cls.deco(name, attr_value)

        return super(LogMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def deco(cls, name, func):
        logger = logging.getLogger('apps.funcall')
        func.ncalls = 0
        def wrapper(self, *args, **kwargs):
            func.ncalls += 1;
            tm = time.time()
            logger.debug("[%s]   call    %s.%s.%s"%(func.ncalls, self.__module__, name, func.__name__))
            res = func(self, *args, **kwargs)
            dtm = time.time() - tm
            logger.debug("[%s] (%.5f) %s.%s.%s"%(func.ncalls, dtm, self.__module__, name, func.__name__))
            return res
        return wrapper

