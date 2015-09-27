# -*- coding: utf8 -*-

from __future__ import absolute_import

from shot_detector.utils.collections import SmartDict

# from .base_point import BasePointState


class BaseVideoState(SmartDict):
    """
        Internal state of video handler at the current moment.
        We fancy video handler like finite state machine.
    """

    # point = BasePointState()

    counters = SmartDict(
        frame=0,
        point=0,
        event=0,
    )

    sliding_windows =  dict()

    pixel_size = None
    colour_size = None

    triggers = SmartDict(
        frame_selected=None,
        point_selected=None,
        event_selected=None,
    )

    options = SmartDict()