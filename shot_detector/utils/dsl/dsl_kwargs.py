# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from functools import wraps


def dsl_kwargs_decorator(*dsl_rules):
    """
    
    :param dsl_rules: 
    :return: 
    """

    def decorator(func):
        """
        
        :param func: 
        :return: 
        """

        @wraps(func)
        def decorated(*args, **kwargs):
            """
            
            :param args: 
            :param kwargs: 
            :return: 
            """
            kwargs = handle_dsl_rules(kwargs, dsl_rules)
            return func(*args, **kwargs)

        return decorated

    return decorator


def handle_dsl_rules(kwargs, dsl_rules):
    """
    
    :param kwargs: 
    :param dsl_rules: 
    :return: 
    """
    for dsl_rule in dsl_rules:
        kwargs = handle_dsl_rules_item(kwargs, dsl_rule)
    return kwargs


def handle_dsl_rules_item(kwargs, dsl_rule):
    """
    
    :param kwargs: 
    :param dsl_rule: 
    :return: 
    """
    assert isinstance(dsl_rule, tuple)

    param = dsl_rule[0]
    types = dsl_rule[1]
    alias_tuple = dsl_rule[2]
    if isinstance(alias_tuple, list):
        alias_tuple = tuple(alias_tuple)
    if not isinstance(alias_tuple, tuple):
        alias_tuple = dsl_rule[2:]
    return replace_kwargs(kwargs, param, types, *alias_tuple)


def replace_kwargs(kwargs, param, types, *alias_tuple):
    """
    Replaces kwargs' names from alias_tuple to param.

    Iterate over `alias_tuple` and pop items from `kwargs`.
    If such name is in the `kwargs` and its type is instance of
    types sets `kwargs[param]` to `kwargs[alias]` value.

    :param dict kwargs: dict of functions parameters.
    :param str param: required name of function parameter.
    :param type types: required type of function parameter.
    :param tuple alias_tuple: a to_tuple of alias to replace
    :rtype: dict
    :return: changed kwargs
    """
    undefined = object()
    alias = undefined
    value = undefined
    for alias in alias_tuple:
        value = kwargs.get(alias, undefined)
        if undefined != value:
            break
    if value != undefined and isinstance(value, types):
        kwargs[param] = value
        kwargs.pop(alias, None)
    return kwargs
