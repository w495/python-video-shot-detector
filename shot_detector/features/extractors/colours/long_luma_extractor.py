# -*- coding: utf8 -*-

from __future__ import absolute_import

from ..base_extractor import BaseExtractor


# noinspection PyAbstractClass
class LongLumaExtractor(BaseExtractor):
    # noinspection PyUnusedLocal
    @staticmethod
    def av_format(**_kwargs):
        return 'gray16le'
