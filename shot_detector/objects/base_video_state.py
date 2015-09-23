# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict

from .obj_dict import ObjDict

from .base_point_state import BasePointState


class BaseVideoState(SmartDict):
    """
        Internal state of video handler at the current moment.
        We fancy video handler like finite state machine.
    """

    point = BasePointState()

    sliding_windows = None

    pixel_size = None
    colour_size  = None

    triggers = SmartDict(
        frame_selected=None,
        point_selected=None,
        event_selected=None,
    )


