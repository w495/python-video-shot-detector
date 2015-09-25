# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import sys
import time

from shot_detector.objects          import SmartDict

from .detectors import CommonDetector
from .features.extractors import ImageBased
from .features.extractors import VectorBased
from .features.extractors.colours import RgbExtractor, LumaExtractor
from .features.filters import BaseFilter
from .selectors.event import BaseEventSelector
from .selectors.point import BasePointSelector
from .settings import start_logging


# from .lib.base_vector_mixin import BaseVectorMixin
# from .lib.base_image_mixin import BaseImageMixin
# from .lib.rgb_colour_mixin import RgbColourMixin
# from .lib.gray_colour_mixin import GrayColourMixin
# from .lib.histogram_mixin import HistogramMixin
# from .lib.intersect_mixin import IntersectMixin
# from .lib.sad_mixin import SadMixin
# from .lib.adv_mixin import AdvMixin
# from .lib.zero_norm_mixin import ZeroNormMixin
# from .lib.l2_norm_mixin import L2NormMixin
# from .lib.threshold_mixin import ThresholdMixin
# from .lib.adaptive_threshold_mixin import AdaptiveThresholdMixin
# from .lib.grad_adaptive_threshold_mixin import GradAdaptiveThresholdMixin
# from .lib.fast_adaptive_threshold_mixin import FastAdaptiveThresholdMixin
# from .lib.optical_flow_mixin import OpticalFlowMixin
# from .lib.normalize_mixin import NormalizeMixin
# class HistIntersectThresholdMixin(HistogramMixin, AdaptiveThresholdMixin,
                                  # IntersectMixin, RgbColourMixin):
    # THRESOLD = 0.8
# class SadThresholdMixin(AdaptiveThresholdMixin, SadMixin, GrayColourMixin):
    # THRESOLD = 0.18
    # pass
# class L2OpticalFlowMixin(AdaptiveThresholdMixin, OpticalFlowMixin, L2NormMixin, GrayColourMixin):
    # pass
# class SimpleImageDetector(SadThresholdMixin, BaseImageMixin, BaseDetector):
    # pass
# class SimpleVectorDetector(SadThresholdMixin, BaseVectorMixin, BaseDetector):
    # pass
# from shot_detector.handlers import BaseVideoHandler, BaseEventHandler, ParallelHandler
class SimpleDetector(
    BaseEventSelector,
    # AdaptiveThresholdFilter,
    LumaExtractor,
    VectorBased,
    CommonDetector,
):
    THRESOLD = 0.19



DEFAULT_FILE_NAME = '/home/w495/Video/Djadja_Stepa Milicioner_96.hi.und.mp4'

DEFAULT_FILE_NAME = '/home/w495/Video/drones/tulum.mp4'



if (__name__ == '__main__'):

    detector = SimpleDetector()

    # # Получаем имя видео-файла.
    video_file_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE_NAME

    t1 = time.time()

    detector.detect(video_file_name, thresold=SimpleDetector.THRESOLD)

    t2 = time.time()
    print (t2 - t1)

