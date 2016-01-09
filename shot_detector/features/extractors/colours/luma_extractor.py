# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from ..base_extractor import BaseExtractor


class LumaExtractor(BaseExtractor):

    # noinspection PyUnusedLocal
    @staticmethod
    def av_format(**_kwargs):
        return 'gray8'
