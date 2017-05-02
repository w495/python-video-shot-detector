# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import logging
from builtins import range

import numpy as np

from shot_detector.utils.numerical import shrink
from .base_extractor import BaseExtractor


class VectorBased(BaseExtractor):
    """
        [frame] ->
            [av_frame] ->
                [formatted av_frame] ->
                    [image] ->
                        [formatted image] ->
                            [features vector]

    """

    __logger = logging.getLogger(__name__)

    # noinspection PyUnusedLocal
    @staticmethod
    def frame_images(av_frame_seq, **_kwargs):

        """

        :type av_frame_seq: collections.Iterable
        :param av_frame_seq:
        :param _kwargs:
        :return:
        """
        for av_frame in av_frame_seq:
            image = av_frame.to_nd_array()
            yield image

    def transform_frame_images(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        image_seq = self.transcode_frame_images(image_seq, **kwargs)
        image_seq = self.format_frame_images(image_seq, **kwargs)
        return image_seq

    def transcode_frame_images(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        return image_seq

    def format_frame_images(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        image_seq = self.shrink_frame_images(image_seq, **kwargs)
        image_seq = self.normalize_frame_images(image_seq, **kwargs)
        return image_seq

    def shrink_frame_images(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        image_size = self.image_size(**kwargs)
        for image in image_seq:
            image = shrink(image * 1.0, image_size.width,
                           image_size.height)
            yield image

    def normalize_frame_images(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        colour_size = self.colour_size(**kwargs)
        for image in image_seq:
            image = image / colour_size
            yield image

    def frame_image_features(self, image_seq, **_kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :param _kwargs:
        :return:
        """
        return image_seq

    def colour_histogram(self, image_seq, histogram_kwargs=None,
                         **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :param histogram_kwargs: dict
        :param kwargs:
        :return:
        """
        if histogram_kwargs is None:
            histogram_kwargs = dict()
        pixel_size = self.pixel_size(**kwargs)
        bins = range(pixel_size + 1)
        for image in image_seq:
            histogram_vector, _bin_edges = np.histogram(
                image,
                bins=histogram_kwargs.get('bins', bins),
                **histogram_kwargs
            )
            yield histogram_vector

    @staticmethod
    def convert_to_luminosity(image_seq, **_kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        for image in image_seq:
            image = np.inner(image, [299, 587, 114]) / 1000.0
            yield image

    @staticmethod
    def normalize_vector(vector):
        """

        :param vector:
        :return:
        """
        rng = vector.max() - vector.min()
        min_ = vector.min()
        return (vector - min_) / rng
