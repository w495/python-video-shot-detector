# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function

from ..base_extractor import BaseExtractor


class LumaExtractor(BaseExtractor):
    """
        ...
    """

    @staticmethod
    def av_format(**_):
        """
        
        :return: 
        """
        return 'rgb24'

    def transcode_frame_images(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :return:
        """
        image_seq = self.convert_to_luminosity(image_seq, **kwargs)
        return image_seq
