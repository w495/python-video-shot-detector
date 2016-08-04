# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import dill


def apply_packed_function_for_map(arg, ):
    (dumped_function, item, args, kwargs) = arg
    """
    Unpack dumped function as target function and call it with arguments.

    :return:
        result of target function
    """
    target_function = dill.loads(dumped_function)
    res = target_function(item, *args, **kwargs)
    return res


def pack_function_for_map(target_function, items, *args, **kwargs):
    """
    Pack function and arguments to object that can be sent from one
    multiprocessing.Process to another. The main problem is:
        «multiprocessing.Pool.map*» or «apply*»
        cannot use class methods or closures.
    It solves this problem with «dill».
    It works with target function as argument, dumps it («with dill»)
    and returns dumped function with arguments of target function.
    For more performance we dump only target function itself
    and don't dump its arguments.
    How to use (pseudo-code):

        ~>>> import multiprocessing
        ~>>> images = [...]
        ~>>> pool = multiprocessing.Pool(100500)
        ~>>> feature = pool.map(
        ~...     *pack_function_for_map(
        ~...         super(Extractor, self).extract_features,
        ~...         images,
        ~...         type='png'
        ~...         **options,
        ~...     )
        ~... )
        ~>>>

    :param target_function:
        function, that you want to execute like
        target_function(item, *args, **kwargs).
    :param items:
        list of items for map
    :param args:
        positional arguments for target_function(item, *args, **kwargs)
    :param kwargs:
        named arguments for target_function(item, *args, **kwargs)
    :return: tuple(function_wrapper, dumped_items)
        It returns a tuple with
            * function wrapper, that unpack and call target function;
            * list of packed target function and its' arguments.
    """
    dumped_function = dill.dumps(target_function)
    dumped_items = [(dumped_function, item, args, kwargs) for item in
                    items]
    return apply_packed_function_for_map, dumped_items


# noinspection PyPep8
class FunctionTask(object):
    """
    Calls function through passing it to another process in a dumped form.
    While creating a `FunctionTask` object we pack constructor arguments
    — target function and its' arguments — to dill-dumped string
    and store it in internal variable.
    While calling the `FunctionTask` we unpack dill-dumped string
    to target function and its' arguments and apply this function to arguments.

    In other words:
    >>> func = lambda x, y: x * y
    >>> ft = FunctionTask(func, 2, 3)
    >>> ft()
    6

    equals to:

    >>> func(2, 3)
    6

    But the main difference is in the moment and place of the call.
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
        func = dumped_dict['func']
        args = dumped_dict['args']
        kwargs = dumped_dict['kwargs']
        self.result = func(*args, **kwargs)
        return self.result
