# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict
from .base_point_state import BasePointState

class BaseVideoState(SmartDict):
    point               = BasePointState()
    options             = SmartDict()
    detector_options    = SmartDict()
    memory_cache        = SmartDict()
    opts                = SmartDict()

