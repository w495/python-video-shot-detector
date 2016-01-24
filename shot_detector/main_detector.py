# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import sys
import time

from .detectors import CommonDetector
from .features.extractors import VectorBased
from .features.extractors.colours import LumaExtractor
from .selectors.event import BaseEventSelector


class SimpleDetector(
        BaseEventSelector,
        LumaExtractor,
        # Histogram,
        # RgbBwExtractor,
        VectorBased,
        CommonDetector,
):
    pass


DEFAULT_FILE_NAME = '/run/media/w495/A2CAE41FCAE3ED8B/home/w495' \
                    '/Videos/Djadja_Stepa Milicioner_96.hi.und.mp4'

# DEFAULT_FILE_NAME = '/home/w495/Video/drones/paris.mp4'
# DEFAULT_FILE_NAME = '/home/w495/Video/drones/tulum.mp4'
# DEFAULT_FILE_NAME = '/home/w495/Video/victoria-global-otsu-256x256.mp4'
# DEFAULT_FILE_NAME = '/home/w495/Video/Bolshie_Glaza_96.lw.und.mp4'
# DEFAULT_FILE_NAME = '/home/w495/Video/naf.mp4'

if __name__ == '__main__':
    detector = SimpleDetector()

    # # Получаем имя видео-файла.
    video_file_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE_NAME

    t1 = time.time()

    detector.detect(video_file_name)

    t2 = time.time()
    print(t2 - t1)
