# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import collections

from shot_detector.utils.log_meta import should_be_overloaded

from .base_frame_handler import BaseFrameHandler


class BasePointHandler(BaseFrameHandler):
    """
        Works with video at point level.
        In this case term «point» is a point in a timeline,
        that can represent some video event or some part of this event.
        Event is a significant point in a timeline.
        The main idea can be represented in scheme:
            [video] => [points] => [points] => [events]
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
                                    -> [events].

        If you want, you can skip some points.
        For this, you should implement `select_point` method.
        Also, you should implement `filter_event_features` 
        and `handle_point` methods.
    """

    __logger = logging.getLogger(__name__)

    def handle_points(self, point_iterable, **kwargs):
        assert isinstance(point_iterable, collections.Iterable)
        feature_iterable = self.point_features(point_iterable, **kwargs)
        event_iterable = self.events(point_iterable, feature_iterable, **kwargs)
        filtered_iterable = self.filter_events(event_iterable, **kwargs)
        handled_iterable = self.handle_events(filtered_iterable, **kwargs)
        return handled_iterable

    @should_be_overloaded
    def point_features(self, point_iterable, **kwargs):

        return point_iterable

    @should_be_overloaded
    def events(self, point_iterable, _feature_iterable, **kwargs):

        return point_iterable

    @should_be_overloaded
    def filter_events(self, event_iterable, **kwargs):

        return event_iterable

    @should_be_overloaded
    def handle_events(self, event_iterable, **kwargs):

        return event_iterable




