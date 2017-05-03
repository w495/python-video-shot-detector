# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import numpy as np

from shot_detector.objects import BasePoint, Second
from .base_shot_detector import BaseShotDetector


class DummyTextDetector(BaseShotDetector):

    def detect(self, input_uri='', format_name=None, **kwargs):
        pass
