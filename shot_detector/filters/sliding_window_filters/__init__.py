# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from .alpha_beta_swfilter import AlphaBetaSWFilter
from .base_combination_swfilter import BaseCombinationSWFilter
from .base_swfilter import BaseSWFilter
from .bspline_swfilter import BsplineSWFilter
from .dct_coef_swfilter import DCTCoefSWFilter
from .dct_linear_regressor_swfilter import DCTLinearRegressorSWFilter
from .dct_regressor_swfilter import DCTRegressorSWFilter
from .debug_grid_swfilter import DebugGridSWFilter
from .debug_swfilter import DebugSWFilter
from .decision_tree_regressor_swfilter import \
    DecisionTreeRegressorSWFilter
from .detrend_swfilter import DetrendSWFilter
from .deviation_difference_swfilter import DeviationDifferenceSWFilter
from .deviation_swfilter import DeviationSWFilter
from .difference_swfilter import DifferenceSWFilter
from .dixon_range_swfilter import DixonRangeSWFilter
from .extrema_swfilter import ExtremaSWFilter
from .ffmpeg_like_treshold_swfilter import FFMpegLikeTresholdSWFilter
from .hist_simple_swfilter import HistSimpleSWFilter
from .kurtosis_swfilter import KurtosisSWFilter
from .level_swfilter import LevelSWFilter
from .mad_swfilter import MadSWFilter
from .max_swfilter import MaxSWFilter
from .mean_swfilter import MeanSWFilter
from .median_swfilter import MedianSWFilter
from .min_std_dct_regression_swfilter import MinStdDCTRegressionSWFilter
from .min_std_mean_swfilter import MinStdMeanSWFilter
from .min_std_otsu_swfilter import MinStdOtsuSWFilter
from .min_std_regression_swfilter import MinStdRegressionSWFilter
from .min_swfilter import MinSWFilter
from .nikitin_swfilter import NikitinSWFilter
from .norm_swfilter import NormSWFilter
from .pack_swfilter import PackSWFilter
from .pearson_correlation_swfilter import PearsonCorrelationSWFilter
from .savitzky_golay_swfilter import SavitzkyGolaySWFilter
from .scale_swfilter import ScaleSWFilter
from .scipy_stat_swfilter import SciPyStatSWFilter
from .shift_swfilter import ShiftSWFilter
from .skewness_swfilter import SkewnessSWFilter
from .stat_test_swfilters import (
    NormalTestSWFilter,
    IndependentStudentTtestSWFilter,
    DependentStudentTtestSWFilter,
    WilcoxonRankSumSWFilter,
    KolmogorovSmirnov2SamplesTestSwfilter,
    StatTestSWFilter,
)
from .std_error_swfilter import StdErrorSWFilter
from .std_swfilter import StdSWFilter
from .variance_swfilter import VarianceSWFilter
from .wiener_swfilter import WienerSWFilter
from .zscore_swfilter import ZScoreSWFilter
from .zscore_zero_swfilter import ZScoreZeroSWFilter
