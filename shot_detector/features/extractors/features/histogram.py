# -*- coding: utf8 -*-

from __future__ import absolute_import

from ..base_extractor import BaseExtractor


class Histogram(BaseExtractor):

    def build_features(self, image, video_state=None, *args, **kwargs):
        """

        :param image:
        :param video_state:
        :param args:
        :param kwargs:
        :return:
        """
        histogram_vector, video_state = self.colour_histogram(
            image,
            video_state
        )

        return histogram_vector, video_state

