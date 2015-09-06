# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict
from .base_point_state import BasePointState

class BaseVideoState(SmartDict):
    '''
        Internal state of video handler at the current moment.
        We fancy video handler like finite state machine.
    '''

    point               = BasePointState()
    options             = SmartDict()
    detector_options    = SmartDict()
    memory_cache        = SmartDict()
    opts                = SmartDict()

