# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from .base_filter import BaseFilter
from .bound_filter import BoundFilter
from .factor_filter import FactorFilter
from .log_filter import LogFilter
from .otsu_filter import OtsuFilter


from .norm_filter import NormFilter
from .sliding_window_filters import BaseCombinationSWFilter
from .sliding_window_filters import BaseSWFilter

from .sliding_window_filters import DifferenceSWFilter
from .sliding_window_filters import DeviationDifferenceSWFilter
from .sliding_window_filters import DeviationSWFilter
from .sliding_window_filters import MaxSWFilter
from .sliding_window_filters import MeanSWFilter
from .sliding_window_filters import MedianSWFilter
from .sliding_window_filters import StdSWFilter
from .sliding_window_filters import ZScoreSWFilter
from .sliding_window_filters import ZScoreZeroSWFilter
from .sliding_window_filters import HistSimpleSWFilter
