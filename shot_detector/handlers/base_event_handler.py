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
            [video] => [frames] => [events] => [summaries]
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
                                    \{extract summaries}
                                    -> [summaries]
                                        \{select summaries}
                    -                   > [some of summaries].

        If you want, you can skip some summaries.
        For this, you should implement `select_summary` method.
        Also, you should implement `handle_summary`.
    """

    __logger = logging.getLogger(__name__)

    def handle_events(self, event_seq, **kwargs):
        assert isinstance(event_seq, collections.Iterable)
        feature_seq = self.event_features(event_seq, **kwargs)
        summary_seq = self.summaries(event_seq, feature_seq, **kwargs)
        filtered_seq = self.filter_summaries(summary_seq, **kwargs)
        handled_seq = self.handle_summaries(filtered_seq, **kwargs)
        return handled_seq

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def event_features(self, event_seq, **_kwargs):
        return event_seq

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def summaries(self, event_seq, _feature_seq, **_kwargs):
        return event_seq

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def filter_summaries(self, event_seq, **_kwargs):
        return event_seq

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def handle_summaries(self, event_seq, **_kwargs):
        return event_seq
