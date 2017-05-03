# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from .base_shot_detector import BaseShotDetector


class DummyTextDetector(BaseShotDetector):

    def detect(self, input_uri='', format_name=None, **kwargs):
        pass
