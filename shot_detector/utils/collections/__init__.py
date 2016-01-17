# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from .condenser import Condenser
from .obj_dict import ObjDict
from .sliding_window import SlidingWindow
from .re_sliding_window import ReSlidingWindow

from .smart_dict import SmartDict

if __name__ == "__main__":
    import doctest
    doctest.testmod()
