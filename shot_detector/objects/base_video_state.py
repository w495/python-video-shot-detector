# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict
from .base_point_state import BasePointState

class BaseVideoState(SmartDict):
    """
        Internal state of video handler at the current moment.
        We fancy video handler like finite state machine.
    """

    point               = BasePointState()
    packet_state        = SmartDict()
    frame_state         = SmartDict()
    sliding_windows     = SmartDict()

    triggers            = SmartDict(
        frame_selected  = None,
        point_selected  = None,
        event_selected  = None,
    )


    options             = SmartDict()
    detector_options    = SmartDict()
    memory_cache        = SmartDict()
    opts                = SmartDict()

