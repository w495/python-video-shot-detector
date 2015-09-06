# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from .base_point_handler  import BasePointHandler

class BaseEventHandler(BasePointHandler):
    '''
        Works with video at event level.
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

        If you want, you can skip some events.
        For this, you should implement `select_event` method.
        Also, you should implement `handle_selected_event`.
    '''

    __logger = logging.getLogger(__name__)

    def handle_event(self, event = None, video_state = None, *args, **kwargs):
        event, video_state = self.select_event(
            event, 
            video_state, 
            *args, 
            **kwargs
        )
        if(event):
            video_state = self.handle_selected_event(
                event, 
                video_state, 
                *args, 
                **kwargs
            )
        return video_state

    def select_event(self, event, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return event, video_state

    def handle_selected_event(self, event, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return video_state

