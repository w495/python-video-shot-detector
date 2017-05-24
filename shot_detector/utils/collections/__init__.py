# -*- coding: utf8 -*-

"""
    Some compound objects like dict and sliding window
"""

from __future__ import absolute_import, division, print_function

from .condenser import Condenser
from .frozen_dict import FrozenDict
from .obj_dict import ObjDict
from .sliding_windows import BaseSlidingWindow
from .sliding_windows import DelayedSlidingWindow
from .sliding_windows import RepeatedSlidingWindow
from .sliding_windows import SlidingWindow
from .smart_dict import SmartDict
from .repr_dict import ReprDict

from .unique import unique
from .object_data_dict import object_data_dict

if __name__ == "__main__":
    import doctest

    doctest.testmod()
