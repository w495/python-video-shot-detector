# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from .base_frame_handler  import BaseFrameHandler


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
                       \{extract features}
                        ->  [raw points] ->
                            \{select points}
                            ->  [some of points] ->
                                \{filter features}
                                ->  [filtered points] ->
                                    \{extract events}
                                    -> [events].

        If you want, you can skip some points.
        For this, you should implement `select_point` method.
        Also, you should implement `filter_event_features` 
        and `handle_point` methods.
    """

    __logger = logging.getLogger(__name__)

    def handle_point(self, point, video_state, *args, **kwargs):
        iterable_point, video_state = self.select_point(
            point,
            video_state,
            *args, **kwargs
        )
        video_state = self.handle_selected_iterable_point(
            iterable_point,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_selected_iterable_point(self, iterable_point, video_state, *args, **kwargs):

        for point in iterable_point:
            video_state.triggers.point_selected = True
            video_state = self.handle_selected_point(
                point,
                video_state,
                *args,
                **kwargs
            )
        else:
            video_state.triggers.point_selected = False
        return video_state

    def handle_selected_point(self, point, video_state, *args, **kwargs):
        iterable_extracted_point_features, video_state = self.extract_point_features(
            point.source,
            video_state,
            *args, **kwargs
        )
        video_state = self.handle_iterable_extracted_point_features(
            iterable_extracted_point_features,
            point,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_iterable_extracted_point_features(self, iterable_features, point, video_state, *args, **kwargs):

        for features in iterable_features:
            video_state = self.handle_extracted_point_features(
                features ,
                point,
                video_state,
                *args, **kwargs
            )
        return video_state

    def handle_extracted_point_features(self, features, point, video_state, *args, **kwargs):
        iterable_features, video_state = self.filter_point_point_features(
            features,
            video_state,
            *args,
            **kwargs
        )
        video_state = self.handle_iterable_filtered_point_features(
            iterable_features,
            point,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_iterable_filtered_point_features(self, iterable_features, point, video_state, *args, **kwargs):
        for features in iterable_features:
            video_state = self.handle_filtered_point_features(
                features ,
                point,
                video_state,
                *args, **kwargs
            )
        return video_state

    def handle_filtered_point_features(self, features, point, video_state, *args, **kwargs):
        raw_event = self.build_event(
            features=features,
            point=point,
        )
        video_state = self.handle_event(
            raw_event,
            video_state,
            *args, **kwargs
        )
        return video_state

    @staticmethod
    def build_event(point, *args, **kwargs):
        return point

    def extract_point_features(self, point, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [point], video_state

    def filter_point_point_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [features], video_state

    def select_point(self, point, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [point], video_state

    def handle_event(self, event, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return video_state



