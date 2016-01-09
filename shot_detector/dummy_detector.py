# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import sys
import time

import numpy as np

from shot_detector.objects import BasePoint, Second
from .detectors import CommonDetector
from .selectors.event import DummyEventSelector


class DummyDetector(
        DummyEventSelector,
        CommonDetector,
):
    def detect(self, file_name, *args, **kwargs):
        video_state = self.build_video_state(**kwargs)
        raw_point_list = np.loadtxt(file_name)
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


DEFAULT_FILE_NAME = 'etc/examples/dummy_shot/djadja-stepa-milicioner.luma4.txt'

if __name__ == '__main__':
    detector = DummyDetector()

    # # Получаем имя видео-файла.
    video_file_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE_NAME

    t1 = time.time()

    detector.detect(video_file_name)

    t2 = time.time()
    print(t2 - t1)
