# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict

class BasePointState(SmartDict):
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
                       \{extract features} 
                        ->  [raw points] -> 
                            \{select points} 
                            ->  [some of points] ->
                                \{filter features}
                                ->  [filtered points] -> 
                                    \{extract events}
                                    -> [events]
                                        \{select events} 
                    -                   > [some of events].
    """

    frame           = None
    timestamp       = None
    features        = None
    value           = None
    skip = None
    point   = None
