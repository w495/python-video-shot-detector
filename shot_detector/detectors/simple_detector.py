# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function



from shot_detector.features.extractors import VectorBased, ParallelExtractor
from shot_detector.features.extractors.colours import LumaExtractor
from shot_detector.plotters.event import (
    RescalingVoteEventPlotter

)

from .common_detector import CommonDetector

class SimpleDetector(
    RescalingVoteEventPlotter,

    # Histogram,
    # RgbBwExtractor,


    LumaExtractor,
    # RgbExtractor,

    #ParallelExtractor,
    VectorBased,

    CommonDetector,
):
    pass











if __name__ == '__main__':
    import time
    FILE_NAME_BASE = '/home/w495/Videos'
    FILE_NAME_REST = 'Djadja_Stepa Milicioner_96.hi.und.mp4'
    file_name = "{}/{}".format(FILE_NAME_BASE, FILE_NAME_REST)
    detector = SimpleDetector()
    t1 = time.time()
    detector.detect(file_name)
    t2 = time.time()
    print(t2 - t1)
