# -*- coding: utf8 -*-

from __future__ import absolute_import

from .base_video_unit import BaseVideoUnit


class BasePoint(BaseVideoUnit):
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
                       \{extract feature}
                        ->  [raw points] -> 
                            \{select points} 
                            ->  [some of points] ->
                                \{filter feature}
                                ->  [filtered points] -> 
                                    \{extract events}
                                    -> [events]
                                        \{select events} 
                    -                   > [some of events].
    """

    feature = None

    undefined_feature = object()


    # @property
    # def feature(self):
    #     return self.__feature
    #
    # @feature.setter
    # def feature(self, value):
    #     self.__feature = value
