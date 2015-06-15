# -*- coding: utf8 -*-

from __future__ import absolute_import

from .settings import start_logging

import sys
import time

from .lib.base_detector import BaseDetector

from .lib.base_vector_mixin import BaseVectorMixin
from .lib.base_image_mixin import BaseImageMixin




from .lib.rgb_colour_mixin import RgbColourMixin
from .lib.gray_colour_mixin import GrayColourMixin

from .lib.histogram_mixin import HistogramMixin
from .lib.intersect_mixin import IntersectMixin



from .lib.sad_mixin import SadMixin
from .lib.zero_norm_mixin import ZeroNormMixin
from .lib.l2_norm_mixin import L2NormMixin


from .lib.threshold_mixin import ThresholdMixin


from .lib.normalize_mixin import NormalizeMixin


class SadThresholdMixin(ThresholdMixin, SadMixin, RgbColourMixin):

    THRESOLD = 0.18
    pass

class HistIntersectThresholdMixin(HistogramMixin, ThresholdMixin, IntersectMixin, RgbColourMixin):

    THRESOLD = 0.8



class SimpleImageDetector(SadThresholdMixin, BaseImageMixin, BaseDetector):
    pass


class SimpleVectorDetector(SadThresholdMixin, BaseVectorMixin, BaseDetector):
    pass


SimpleDetector = SimpleVectorDetector


DEFAULT_FILE_NAME = './15sec.hd.mp4'

if (__name__ == '__main__'):


    detector = SimpleDetector()

    ## Получаем имя видео-файла.
    video_file_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE_NAME


    t1 = time.time()

    detector.detect(video_file_name, thresold = SimpleDetector.THRESOLD)

    t2 = time.time()
    print t2 - t1
