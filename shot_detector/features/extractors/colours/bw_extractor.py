# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from shot_detector.utils.numerical import threshold_otsu
from ..base_extractor import BaseExtractor


# noinspection PyAbstractClass
class BwExtractor(BaseExtractor):
    # noinspection PyUnusedLocal
    @staticmethod
    def av_format(**_kwargs):
        return 'rgb24'

    def transcode_frame_images(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        image_seq = self.convert_to_luminosity(image_seq, **kwargs)
        image_seq = self.threshold_otsu_frame_images(image_seq,
                                                     **kwargs)
        return image_seq

    # noinspection PyUnusedLocal
    @staticmethod
    def threshold_otsu_frame_images(image_seq, **_kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        for image in image_seq:
            yield threshold_otsu(image)
