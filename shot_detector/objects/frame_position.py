# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from shot_detector.utils import ReprDict



class FramePosition(object):
    """
        ...
    """

    __slots__ = [
        'global_number',
        'frame_number',
        'packet_number',
    ]

    def __init__(self,
                 position=None,
                 global_number=None,
                 frame_number=None,
                 packet_number=None):
        """
        
        :param width: 
        :param height: 
        """
        if position:
            self.global_number = position.global_number
            self.frame_number = position.frame_number
            self.packet_number = position.packet_number

        self.global_number = global_number
        self.frame_number = frame_number
        self.packet_number = packet_number



    def __repr__(self):
        return "{p}:{f} ({g})".format(
            p=self.packet_number,
            f=self.frame_number,
            g=self.global_number,
        )

    def repr_dict(self):
        repr_dict = ReprDict(type(self), self)
        return repr_dict