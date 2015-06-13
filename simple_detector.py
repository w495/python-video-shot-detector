# -*- coding: utf8 -*-

from __future__ import absolute_import

import sys
import time

from .lib.base_detector import BaseDetector
from .lib.rgb_image_mixin import RgbImageMixin
from .lib.histogram_mixin import HistogramMixin


from .settings import start_logging

class SimpleDetector(RgbImageMixin, HistogramMixin, BaseDetector):
    pass


import logging




if (__name__ == '__main__'):
    start_logging()

    detector = SimpleDetector()

    ## Получаем имя видео-файла.
    #video_file_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE_NAME

    video_file_name  = './v.hi.und.mp4'


    t1 = time.time()

    detector.detect(video_file_name)

    t2 = time.time()
    print t2 - t1
