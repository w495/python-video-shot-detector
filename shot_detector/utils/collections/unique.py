# -*- coding: utf8 -*-

"""
    Some compound objects like dict and sliding window
"""

from __future__ import absolute_import, division, print_function


def unique(seq):
    """
        Remove duplicates. Preserve order first seen.
        Assume orderable, but not hashable elements
    """
    return tuple(iter_unique(seq))


def iter_unique(seq):
    """
        Remove duplicates. Preserve order first seen.
        Assume orderable, but not hashable elements
    """
    seen = []
    for item in seq:
        index = bisect_left(seen, item)
        if index == len(seen) or seen[index] != item:
            seen.insert(index, item)
            yield item
