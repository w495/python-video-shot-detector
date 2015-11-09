# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function


import sys
import time

from .detectors import CommonDetector

from .selectors.event import DummyEventSelector

from .settings import start_logging


from shot_detector.objects import BasePoint, Second

import numpy as np


class DummyDetector(
    DummyEventSelector,
    CommonDetector,
):

    def detect(self, video_file_name, *args, **kwargs):
        video_state =  self.build_video_state(*args, **kwargs)
        raw_point_list = np.loadtxt(video_file_name)
        for number, raw_point in enumerate(raw_point_list):
            point = BasePoint(
                features=raw_point,
                source=raw_point,
                time=Second(number),
                global_number=number,
                frame_number = number,
                packet_number =0,
            )
            self.select_event(point, video_state)

        self.diff_plot.plot_data()

        print (video_state)




DEFAULT_FILE_NAME='etc/examples/dummy_shot/djadja-stepa-milicioner.luma2.txt'


if (__name__ == '__main__'):

    detector = DummyDetector()

    # # Получаем имя видео-файла.
    video_file_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE_NAME

    t1 = time.time()

    detector.detect(video_file_name)

    t2 = time.time()
    print (t2 - t1)

