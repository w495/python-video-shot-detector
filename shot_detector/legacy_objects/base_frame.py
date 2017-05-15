# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import

from .base_video_unit import BaseVideoUnit


class BaseFrame(BaseVideoUnit):
    """
        Abstract structure, a point in a timeline,
        that can represent some video event or some part of this event.
        Event is a significant point in a timeline.
        The main idea can be represented in scheme:
            [video] => [frames] => [points] => [events]
        OR:
            [video] -> 
                \{extract frames} 
                ->  [raw frames] -> 
                    \{select frames} 
                    -> [some of frames] -> 
                       \{extract frame_number} 
                        ->  [raw points] -> 
                            \{select points} 
                            ->  [some of points] ->
                                \{filter frame_number}
                                ->  [filtered points] -> 
                                    \{extract events}
                                    -> [events]
                                        \{select events} 
                    -                   > [some of events].
    """

    __frame_number = None

    __packet_number = None

    @property
    def frame_number(self):
        """
        
        :return: 
        """
        return self.__frame_number

    @frame_number.setter
    def frame_number(self, value):
        """
        
        :param value: 
        :return: 
        """
        self.__frame_number = value

    @property
    def packet_number(self):
        """
        
        :return: 
        """
        return self.__packet_number

    @packet_number.setter
    def packet_number(self, value):
        """
        
        :param value: 
        :return: 
        """
        self.__packet_number = value
