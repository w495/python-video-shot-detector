# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from scipy.fftpack import dct

from ..base_extractor import BaseExtractor


# noinspection PyAbstractClass
class Dct(BaseExtractor):
    def frame_image_features(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :param kwargs:
        :return:
        """

        for image in image_seq:
            yield dct(image)
