# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from .angle_change_filter import AngleChangeFilter
from .base_filter import BaseFilter
from .base_nested_filter import BaseNestedFilter
from .bound_filter import BoundFilter
from .colour_filter import ColourFilter
from .condition_filter import ConditionFilter
from .dct_filter import DCTFilter
from .delay_filter import DelayFilter
from .dht_filter import DHTFilter
from .exp_filter import ExpFilter
from .factor_filter import FactorFilter
from .filter import Filter
from .filter_operator import FilterOperator
from .join_filter import JoinFilter
from .log_filter import LogFilter
from .modulus_filter import ModulusFilter
from .norm_filter import NormFilter
from .otsu_filter import OtsuFilter
from .sign_change_filter import SignChangeFilter
from .slice_filter import SliceFilter
from .sliding_window_filters import (
    AlphaBetaSWFilter,
    BaseCombinationSWFilter,
    DetrendSWFilter,
    BaseSWFilter,
    BsplineSWFilter,
    SavitzkyGolaySWFilter,
    WienerSWFilter,
    NikitinSWFilter,
    PearsonCorrelationSWFilter,
    DCTCoefSWFilter,
    DCTLinearRegressorSWFilter,
    DCTRegressorSWFilter,
    DecisionTreeRegressorSWFilter,
    DeviationDifferenceSWFilter,
    DeviationSWFilter,
    DifferenceSWFilter,
    ExtremaSWFilter,
    DixonRangeSWFilter,
    HistSimpleSWFilter,
    LevelSWFilter,
    MadSWFilter,
    MaxSWFilter,
    MeanSWFilter,
    MedianSWFilter,
    MinSWFilter,
    ScaleSWFilter,
    ShiftSWFilter,
    StdSWFilter,
    StdErrorSWFilter,
    ZScoreSWFilter,
    ZScoreZeroSWFilter,
    MinStdMeanSWFilter,
    SkewnessSWFilter,
    KurtosisSWFilter,
    VarianceSWFilter,
    NormalTestSWFilter,
    DebugGridSWFilter,  # only for debugging
    DebugSWFilter,  # only for debugging
    IndependentStudentTtestSWFilter,
    DependentStudentTtestSWFilter,
    WilcoxonRankSumSWFilter,
    KolmogorovSmirnov2SamplesTestSwfilter,
    StatTestSWFilter,
    PackSWFilter,
    MinStdRegressionSWFilter,
    MinStdDCTRegressionSWFilter,
    MinStdOtsuSWFilter,
    FFMpegLikeTresholdSWFilter,
    NormSWFilter,
)
