# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import itertools


# noinspection PyPep8
def handle_content(iterable, unpack=None, handle=None, pack=None, *args, **kwargs):
    """
    Handle each item of iterable in pipeline (!) like this:
        content         = unpack_item(item)
        handled_content = handle_item(content)
        item            = pack_item(item, handled_content)

    :param iterable: some sequence
    :param args:    additional positional arguments, that passes to all of (unpack, handle, pack)
    :param kwargs:  additional named arguments, that passes to all of (unpack, handle, pack)
    :return: new iterable with handled content in each item

    Steps of pipeline represented by functions
    :param unpack: function(iterable, *args, **kwargs) or None
    :param handle: function(iterable, *args, **kwargs) or None
    :param pack:   function(iterable, iterable, *args, **kwargs) or None

    If one of the functions is None, this step of pipeline will be skipped.

    So the main scheme of handling:
        content_iterable = unpack(orig_iterable)
        handled_iterable = handle(content)
        result_iterable  = pack_item(orig_iterable, handled_iterable)

    Example:
        >>> def get(iterable):
        ...     for item in iterable:
        ...         yield item.get('value', 0)
        >>>
        >>> def fun(iterable):
        ...     for item in iterable:
        ...         yield item * 2
        >>>
        >>> def set_(iterable, values):
        ...     # zip = itertools.izip
        ...     for item, value in zip(iterable, values):
        ...         item['value'] = value
        ...         yield item
        >>>
        >>> data = [dict(name='x', value=1), dict(name='y', value=2)]
        >>>
        >>> list(handle_content(data, get, fun, set_))
        [{'name': 'x', 'value': 2}, {'name': 'y', 'value': 4}]
        >>>
    """


    return handle_content_sequential(
        iterable,
        unpack,
        handle,
        pack,
        *args,
        **kwargs
    )


def handle_content_sequential(iterable,
                              unpack=None,
                              handle=None,
                              pack=None,
                              *args,
                              **kwargs):

    if unpack is None:
        unpack = __default_unpack
    if handle is None:
        handle = __default_handle
    if pack is None:
        pack = __default_pack

    iterable = iter(iterable)
    items, orig_items = itertools.tee(iterable)
    contents = unpack(items, *args, **kwargs)
    handled_contents = handle(contents, *args, **kwargs)
    packed = pack(orig_items, handled_contents, *args, **kwargs)
    return packed


# noinspection PyUnusedLocal
def __default_unpack(x, **_kw):
    return x


# noinspection PyUnusedLocal
def __default_handle(x, **_kw):
    return x


# noinspection PyUnusedLocal
def __default_pack(x, **_kw):
    return x
