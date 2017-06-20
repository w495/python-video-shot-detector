# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from shot_detector.charts.event import (
    RescalingVoteEventChart
)
from shot_detector.features.extractors import VectorBased
from shot_detector.features.extractors.colours import LumaExtractor
from .common_detector import CommonDetector


class SimpleDetector(
    RescalingVoteEventChart,
    LumaExtractor,

    VectorBased,

    CommonDetector,
):
    """
        ...
    """
    pass
