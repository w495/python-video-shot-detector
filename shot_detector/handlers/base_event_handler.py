# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import logging

from shot_detector.utils.log_meta import should_be_overloaded
from .base_point_handler import BasePointHandler


class BaseEventHandler(BasePointHandler):
    """
        Works with video at summary level.
        Event is a significant event in a timeline.
        The main idea can be represented in scheme:
            [video] => [frames] => [events] => [summarys]
        OR:
            [video] ->
                \{extract frames}
                ->  [raw frames] ->
                    \{select frames}
                    -> [some of frames] ->
                       \{extract feature}
                        ->  [raw events] ->
                            \{select events}
                            ->  [some of events] ->
                                \{filter feature}
                                ->  [filtered events] ->
                                    \{extract summarys}
                                    -> [summarys]
                                        \{select summarys}
                    -                   > [some of summarys].

        If you want, you can skip some summarys.
        For this, you should implement `select_summary` method.
        Also, you should implement `handle_summary`.
    """

    __logger = logging.getLogger(__name__)

    def handle_events(self, event_iterable, **kwargs):
        assert isinstance(event_iterable, collections.Iterable)
        feature_iterable = self.event_features(event_iterable, **kwargs)
        summary_iterable = self.summaries(event_iterable, feature_iterable, **kwargs)
        filtered_iterable = self.filter_summaries(summary_iterable, **kwargs)
        handled_iterable = self.handle_summaries(filtered_iterable, **kwargs)
        return handled_iterable

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def event_features(self, event_iterable, **_kwargs):
        return event_iterable

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def summaries(self, event_iterable, **_kwargs):
        return event_iterable

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def filter_summaries(self, event_iterable, **_kwargs):
        return event_iterable

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def handle_summaries(self, event_iterable, **_kwargs):
        return event_iterable
