# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict
from .base_cut_state import BaseCutState

class BaseVideoState(SmartDict):
    curr                = BaseCutState()
    prev                = BaseCutState()
    options             = SmartDict()
    detector_options    = SmartDict()
    memory_cache        = SmartDict()
    opts                = SmartDict()
    cut_list            = []
    cut_counter         = 0

