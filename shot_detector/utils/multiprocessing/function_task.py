# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import dill
import logging

from shot_detector.utils.collections import SmartDict


class FunctionTask(object):
    """
    Тask that call function

    """

    __logger = logging.getLogger(__name__)

    def __init__(self, func, *args, **kwargs):
        """
        Creates FunctionTask object.
        Pack triple `(func, *args, **kwargs)` into dill-dumped object
        to send it to another process.

        :param func: function or method
            function, that you want to execute like  func(*args, **kwargs).
        :param args:
            positional arguments of function `func`.
        :param kwargs:
            named arguments of function `func`.
        """

        self.dumped_data = dill.dumps(dict(
            func=func,
            args=args,
            kwargs=kwargs,
        ))
        self.result = None

    def __call__(self):
        """
        Unpack dill-dumped object into triple `(func, *args, **kwargs)`
        and execute `func(*args, **kwargs)`

        :return: any
            result of func(*args, **kwargs).
        """
        dumped_dict = dill.loads(self.dumped_data)
        obj = SmartDict(dumped_dict)
        self.result = obj.func(*obj.args, **obj.kwargs)
        return self.result
