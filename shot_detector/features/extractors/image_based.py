# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from PIL import Image

from .base_extractor import BaseExtractor

AV2PIL_FORMAT_DICT = dict(
    gray='L',
    gray16le='L',
    rgb24='RGB'
)


class ImageBased(BaseExtractor):
    def frame_images(self, av_frame_seq, **kwargs):
        """

        :type av_frame_seq: collections.Iterable
        :param av_frame_seq:
        :return:
        """
        pil_format = self.pil_format(**kwargs)
        for av_frame in av_frame_seq:
            plane = av_frame.planes[0]
            # noinspection PyArgumentEqualDefault
            image = Image.frombuffer(
                pil_format,
                (av_frame.width, av_frame.height),
                plane,
                'raw',
                pil_format,
                0,
                1
            )
            yield image

    def pil_format(self, pil_format=None, **kwargs):
        av_format = self.av_format(**kwargs)
        if pil_format is None:
            pil_format = AV2PIL_FORMAT_DICT.get(av_format, 256)
        return pil_format

    def colour_histogram(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :param kwargs:
        :return:
        """
        for image in image_seq:
            histogram_vector = image.histogram()
            yield histogram_vector

    @staticmethod
    def convert_to_luminosity(image_seq, **_kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        for image in image_seq:
            image = image.convert('L')
            yield image
