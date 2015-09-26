# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from .base_point_handler  import BasePointHandler

class BaseEventHandler(BasePointHandler):
    """
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
        Also, you should implement `handle_summary`.
    """

    __logger = logging.getLogger(__name__)

    def handle_event(self, event, video_state, *args, **kwargs):
        iterable_event, video_state = self.select_event(
            event,
            video_state,
            *args, **kwargs
        )
        video_state = self.handle_selected_iterable_event(
            iterable_event,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_selected_iterable_event(self, iterable_event, video_state, *args, **kwargs):

        for event in iterable_event:
            video_state.triggers.event_selected = True
            video_state = self.handle_selected_event(
                event,
                video_state,
                *args,
                **kwargs
            )
        else:
            video_state.triggers.event_selected = False
        return video_state

    def handle_selected_event(self, event, video_state, *args, **kwargs):
        iterable_extracted_event_features, video_state = self.extract_event_features(
            event.source,
            video_state,
            *args, **kwargs
        )
        video_state = self.handle_iterable_extracted_event_features(
            iterable_extracted_event_features,
            event,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_iterable_extracted_event_features(self, iterable_features, event, video_state, *args, **kwargs):

        for features in iterable_features:
            video_state = self.handle_extracted_event_features(
                features ,
                event,
                video_state,
                *args, **kwargs
            )
        return video_state

    def handle_extracted_event_features(self, features, event, video_state, *args, **kwargs):
        iterable_features, video_state = self.filter_event_event_features(
            features,
            video_state,
            *args,
            **kwargs
        )
        video_state = self.handle_iterable_filtered_event_features(
            iterable_features,
            event,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_iterable_filtered_event_features(self, iterable_features, event, video_state, *args, **kwargs):
        for features in iterable_features:
            video_state = self.handle_filtered_event_features(
                features ,
                event,
                video_state,
                *args, **kwargs
            )
        return video_state

    def handle_filtered_event_features(self, features, event, video_state, *args, **kwargs):
        raw_summary = self.build_summary(
            features=features,
            event=event,
        )
        video_state = self.handle_summary(
            raw_summary,
            video_state,
            *args, **kwargs
        )
        return video_state

    @staticmethod
    def build_summary(event, *args, **kwargs):
        return event

    def extract_event_features(self, event, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [event], video_state

    def filter_event_event_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [features], video_state

    def select_event(self, event, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [event], video_state

    def handle_summary(self, summary, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return video_state



