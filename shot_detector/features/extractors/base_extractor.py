# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections

from shot_detector.handlers import BaseFrameHandler
from shot_detector.objects import BaseFrame, BaseFrameSize
from shot_detector.utils.log_meta import should_be_overloaded

# #
# # Size of vector, when we deal with computing.
# # For optimization issues it should be multiple by 2.
# # Perhaps it is better to put in `video_state`.
# #
DEFAULT_IMAGE_SIZE = BaseFrameSize(
    width=2,
    height=2,
)

# #
# # For optimization issues it should be multiple by 8.
# # Perhaps it is better to put in `video_state`.
# #
DEFAULT_OPTIMIZE_FRAME_SIZE = BaseFrameSize(
    width=16,
    height=16,
)

DEFAULT_AV_FORMAT = 'rgb24'

AV_FORMAT_COLOUR_SIZE = dict(
    rgb24=(1 << 8),
    gray16le=(1 << 16),
)

AV_FORMAT_PIXEL_SIZE_COEF = dict(
    rgb24=3,
    gray16le=1,
)


class BaseExtractor(BaseFrameHandler):
    """
        [frame] ->
            [av_frame] ->
                [formatted av_frame] ->
                    [image] ->
                        [formatted image] ->
                            [features vector]

    """

    def frame_features(self, frame_seq, **kwargs):
        """

        :type frame_seq: collections.Iterable
        :param frame_seq:
        :param kwargs:
        :return:
        """
        assert isinstance(frame_seq, collections.Iterable)
        frame_seq = self.av_frames(frame_seq, **kwargs)
        frame_seq = self.format_av_frames(frame_seq, **kwargs)
        image_seq = self.frame_images(frame_seq, **kwargs)
        image_seq = self.transform_frame_images(image_seq, **kwargs)
        feature_seq = self.frame_image_features(image_seq, **kwargs)
        return feature_seq

    # noinspection PyUnusedLocal
    @staticmethod
    def av_frames(frame_seq, **_kwargs):
        """

        :type frame_seq: collections.Iterable
        :param frame_seq:
        :return:
        """
        return BaseFrame.source_sequence(frame_seq)

    def format_av_frames(self, frame_seq, **kwargs):
        """

        :type frame_seq: collections.Iterable
        :param frame_seq:
        :return:
        """
        av_format = self.av_format(**kwargs)
        frame_size = self.frame_size(**kwargs)
        for av_frame in frame_seq:
            yield av_frame.reformat(
                format=av_format,
                width=frame_size.width,
                height=frame_size.height,
            )

    #
    # Size methods
    #

    # noinspection PyUnusedLocal
    @staticmethod
    def av_format(av_format=None, **_kwargs):
        if av_format is None:
            av_format = DEFAULT_AV_FORMAT
        return av_format

    # noinspection PyUnusedLocal
    def colour_size(self, colour_size=None, **kwargs):
        """

        :param colour_size:
        :param kwargs:
        :return:
        """
        av_format = self.av_format(**kwargs)
        if colour_size is None:
            colour_size = AV_FORMAT_COLOUR_SIZE.get(av_format, 256)
        return colour_size

    # noinspection PyUnusedLocal
    def pixel_size_coef(self, pixel_size_coef=None, **kwargs):
        av_format = self.av_format(**kwargs)
        if pixel_size_coef is None:
            pixel_size_coef = AV_FORMAT_PIXEL_SIZE_COEF.get(av_format,
                                                            256)
        return pixel_size_coef

    def pixel_size(self, **kwargs):
        colour_size = self.colour_size(**kwargs)
        pixel_size_coef = self.pixel_size_coef(**kwargs)
        return colour_size * pixel_size_coef

    # noinspection PyUnusedLocal
    @staticmethod
    def frame_size(frame_size=None, **_kwargs):
        if frame_size is None:
            frame_size = DEFAULT_OPTIMIZE_FRAME_SIZE
        return frame_size

    # noinspection PyUnusedLocal
    @staticmethod
    def image_size(image_size=None, **_kwargs):
        if image_size is None:
            image_size = DEFAULT_IMAGE_SIZE
        return image_size

    #
    # Methods that should be overloaded
    #

    # noinspection PyUnusedLocal
    @staticmethod
    @should_be_overloaded
    def frame_images(frame_seq, **_kwargs):
        """

        :type frame_seq: collections.Iterable
        :param frame_seq:
        :param _kwargs:
        :return:
        """
        raise NotImplementedError(
            'this is interface method `frame_images`: must be implemented')

    @staticmethod
    @should_be_overloaded
    def transform_frame_images(image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        return image_seq

    @staticmethod
    @should_be_overloaded
    def frame_image_features(image_seq, **_kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :param _kwargs:
        :return:
        """
        return image_seq

    #
    # Methods for calculating image features
    #
    @staticmethod
    @should_be_overloaded
    def colour_histogram(image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :param kwargs:
        :return:
        """
        raise NotImplementedError(
            'this is interface method `colour_histogram`: must be implemented')

    @staticmethod
    @should_be_overloaded
    def convert_to_luminosity(image_seq, **_kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        return image_seq

    @staticmethod
    @should_be_overloaded
    def normalize_vector(vector):
        """

        :param vector:
        :return:
        """
        return vector
