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
