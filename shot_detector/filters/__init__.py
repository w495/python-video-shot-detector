# -*- coding: utf8 -*-

"""
    Filter collection
"""

from __future__ import absolute_import, division, print_function

from .common import (
    AtanFilter,
    BoundFilter,
    ColourFilter,
    DCTFilter,
    DHTFilter,
    ExpFilter,
    FactorFilter,
    FloorFilter,
    LogFilter,
    ModulusFilter,
    NormFilter,
    OtsuFilter,
    SignAngleDiff1DFilter,
    SignAngleDiff2DFilter,
    SignChangeFilter,
)
from .filter import Filter
from .sliding_window import (
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
    KolmogorovSmirnov2SamplesTestSWFilter,
    StatTestSWFilter,
    PackSWFilter,
    MinStdRegressionSWFilter,
    MinStdDCTRegressionSWFilter,
    MinStdOtsuSWFilter,
    FFMpegLikeThresholdSWFilter,
    NormSWFilter
)
from .util import (
    ConditionFilter,
    DelayFilter,
    BulkFilter,
    ForkFilter,
)
