# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import sys
import time

import numpy as np

from shot_detector.objects import BasePoint, Second
from .base_shot_detector import BaseShotDetector


class DummyTextDetector(BaseShotDetector):

    def detect(self, input_uri='', format_name=None, **kwargs):
        video_state = self.build_video_state(**kwargs)
        raw_point_list = np.loadtxt(input_uri)
        for number, raw_point in enumerate(raw_point_list):
            point = BasePoint(
                features=np.array([raw_point]),
                source=raw_point,
                time=Second(number),
                global_number=number,
                frame_number=number,
                packet_number=0,
            )
            self.select_event(point, video_state)

        self.diff_plot.plot_data()

        print(video_state)
