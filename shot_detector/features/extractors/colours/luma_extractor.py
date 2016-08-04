# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from ..base_extractor import BaseExtractor


# noinspection PyAbstractClass
class LumaExtractor(BaseExtractor):
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
        return image_seq
