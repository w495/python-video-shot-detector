# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import itertools
import logging

from shot_detector.filters import (
    DelayFilter,
    MinStdMeanSWFilter,
    NikitinSWFilter,
    AlphaBetaSWFilter,
    BsplineSWFilter,
    DetrendSWFilter,
    SavitzkyGolaySWFilter,
    WienerSWFilter,
    MedianSWFilter,
    ExtremaSWFilter,
    PearsonCorrelationSWFilter,
    ShiftSWFilter,
    LevelSWFilter,
    MeanSWFilter,
    NormFilter,
    DeviationSWFilter,
    StdSWFilter,
    DecisionTreeRegressorSWFilter,
    ModulusFilter,
    DCTFilter,
    DixonRangeSWFilter,
    DHTFilter,
    LogFilter,
    ExpFilter,
    MaxSWFilter,
    MinSWFilter,
    ZScoreSWFilter,
    DCTRegressorSWFilter,
    ScaleSWFilter,
    StdErrorSWFilter,
    DCTCoefSWFilter,
    KurtosisSWFilter,
    SkewnessSWFilter,
    NormalTestSWFilter,
    FFMpegLikeTresholdSWFilter,

    StatTestSWFilter,
    MadSWFilter,
    MinStdRegressionSWFilter,
    MinStdOtsuSWFilter,
    ColourFilter,
    SignChangeFilter

)
from shot_detector.filters import (
    mean_cascade
)
from shot_detector.handlers import BaseEventHandler, BasePlotHandler
from shot_detector.utils.collections import SmartDict

sgn_changes = SignChangeFilter(

)

norm = NormFilter(
)

fabs = ModulusFilter()

dct = DCTFilter()

dht = DHTFilter()

log = LogFilter()

exp = ExpFilter()

colour = ColourFilter()

extrema = ExtremaSWFilter(
    strict_windows=True,
    overlap_size=0,
    cs=False,
)

delay = DelayFilter()

original = delay(0)

savgol = SavitzkyGolaySWFilter(
    window_size=50,
    strict_windows=True,
    overlap_size=0,
    # cs=False
)

wiener = WienerSWFilter(
    window_size=50,
    strict_windows=True,
    overlap_size=0,
)

alpha_beta = AlphaBetaSWFilter(
    window_size=50,
    strict_windows=True,
    overlap_size=0,
)

corr = PearsonCorrelationSWFilter(
    window_size=10,
    strict_windows=True,
    # overlap_size=0,
    # repeat_windows=True,
)

fmax = MaxSWFilter(
    window_size=25,
    strict_windows=True,
)

fmin = MinSWFilter(
    window_size=25,
    strict_windows=True,
)

zscore = ZScoreSWFilter(
    window_size=25,
    sigma_num=3,
    cs=False,
)

deviation = DeviationSWFilter(
    window_size=25,
    std_coef=2.5,
)

shift = ShiftSWFilter(
    window_size=2,
    strict_windows=False,
    cs=False,
)

level = LevelSWFilter(
    level_number=10000,
    global_max=1.0,
    global_min=0.0,
)

adaptive_level = LevelSWFilter(
    level_number=100,
    window_size=50,
)

median = MedianSWFilter(
    window_size=5,
    strict_windows=True,
)

mean = MeanSWFilter(
    window_size=25,
    # strict_windows=True,
    cs=False
)

ewma = MeanSWFilter(
    window_size=50,
    # strict_windows=True,
    mean_name='EWMA',
    cs=False
)

std = StdSWFilter(
    window_size=25,
    strict_windows=True,
)

std_error = StdErrorSWFilter(
    window_size=25,
    strict_windows=True,
)

dtr = DecisionTreeRegressorSWFilter(
    window_size=100,
    strict_windows=True,
    overlap_size=0,
    cs=False,
)

sad = original - shift

deviation = original - mean

dct_re = DCTRegressorSWFilter(
    window_size=25,
    strict_windows=True,
    overlap_size=0,
)

dct_coef = DCTCoefSWFilter(
    window_size=25,
    strict_windows=True,
)

scale = ScaleSWFilter(
    s=25 * 20,
    strict_windows=True,
    overlap_size=0,
)

bspline = BsplineSWFilter(
    window_size=4,
    strict_windows=True,
    overlap_size=0,
)

smooth = dtr(s=25 * 32, d=5) | savgol(s=25 * 32)

nikitin_1 = NikitinSWFilter(
    window_size=256,
    depth=5,
    strict_windows=True,
    overlap_size=0,
    cs=False,
)

detrend = DetrendSWFilter(
    window_size=25 * 8,
    strict_windows=True,
    overlap_size=0,
)

msm = MinStdMeanSWFilter(
    window_size=25,
    min_size=2
)

kurtosis = KurtosisSWFilter(
    window_size=25,
    strict_windows=True,
)

skewness = SkewnessSWFilter(
    window_size=25,
    strict_windows=True,
)

normaltest = NormalTestSWFilter(
    window_size=20,
    overlap_size=0,
    repeat_windows=True,
    strict_windows=True,
)

# frange = (fmax - fmin) / mean


stat_test = StatTestSWFilter(
    window_size=25,
    strict_windows=True,
    # overlap_size=0,
    # repeat_windows=True
    # cs=False,
)

mad = MadSWFilter(
    window_size=25,
    overlap_size=0,
    repeat_windows=True
    # cs=False,
)

dixon_r = DixonRangeSWFilter(
    window_size=5,
    strict_windows=True,
    cs=False,
)

# mean | sad | sad | fabs  — разладко по определению.

# nikitin = median | mean | nikitin_1 * 10

# nikitin = (sad | fabs | deviation) < (sad | fabs)

#
# nikitin =  dct_re(last=10) # nikitin_1(use_first = True)

# nikitin =  std / mean  # — very cool

# nikitin = mean | skewness(s=25) / 10


# nikitin = norm(l=2) | (normaltest < 0.1) —— cool as periods of
# annormal distribution.

#
# Very cool way to get outlier
#   nikitin = norm(l=1) | sad | original - median(s=25) | fabs
#
#   nikitin = norm(l=1) | original - median(s=25) | fabs
# Use with extrema(s=100, x=1.1, order=50),
#

#
# Strange
# nikitin = norm(l=1) | (dixon_r > 0.9)
#

##
# Very cool
# nikitin = norm(l=1) | original - savgol(s=25) | fabs | mean(s=10)
#

##
# Very-very cool but slow
#
#
# def multi_savgol(begin=9, end=61):
#     res = 0
#     cnt = 0
#     for size in xrange(begin, end, 2):
#         res += (original - savgol(s=size))
#         cnt += 1
#     return (res/cnt)
#
#
# nikitin = norm(l=1) | multi_savgol() | fabs | zscore


#
# Normal, a bit strage. ~Marchuk-style (pp 10)
#
#
# def multi_savgol_with_bills(begin=9, end=25, esp=6):
#     res = 0
#     cnt = 0
#     for size in xrange(begin, end, 2):
#         delta = original - savgol(s=size) | abs
#         bill = delta | (original > (esp * std(s=end))) | int
#         res += bill
#         cnt += 1
#     res_mean = res | mean(s=100)
#     res = (res > res_mean) | int
#     return (res)
#
#
# nikitin = norm(l=1) | multi_savgol_with_bills()


# def multi_mean(begin=9, end=61):
#     res = 0
#     cnt = 0
#     for size in xrange(begin, end, 2):
#         print()
#         res += (original - mean(s=size))
#         cnt += 1
#     return (res/cnt)
#
#
# nikitin = norm(l=1) | multi_mean() | original - median | abs
#
#
# nikitin9 = norm(l=1) | original - mean(s=9) | original - median | abs
#
# nikitin61 = norm(l=1) | original - mean(s=61) | original - median | abs

# import sys
# sys.setrecursionlimit(100000)


mstd = MinStdMeanSWFilter(
    window_size=100,
    strict_windows=True,
    overlap_size=0,
    repeat_windows=True,
    cs=False,
)

mstdotsu = MinStdOtsuSWFilter(
    window_size=100,
    strict_windows=True,
    overlap_size=0,
    cs=False,
)

msr = MinStdRegressionSWFilter(
    window_size=100,
    strict_windows=True,
    overlap_size=0,
    cs=False,
)

# fdelta = norm(l=1) | min_std_cascade.multi_dtr() | abs
#
# nikitin = fdelta | (original > 6*std(s=25)) | int
#
# sigma3 = original > (mean(s=50) + 3*std(s=50))
#
# nikitin9 = norm(l=1) | mean(s=10) - mean(s=20) | abs | sigma3  | int


# diff = original - shift
# sigma3 = original > (mean(s=50) + 3*std(s=50))
# nikitin = norm(l=1) | diff | abs | sigma3 | int
#
#
# nikitin9 = (norm(l=1)
#             | original - mole_filter()
#             | abs
#             | sigma3
#             | int) | original * 0.9


# std_x = dct_re(last=2) # nikitin_1(use_first = True) | std
#
# std_x = norm(l=1) | sad


ffmpeglike = FFMpegLikeTresholdSWFilter()


def sigma3(c=3.0, **kwargs):
    return (
               original
               > (
                   mean(**kwargs)
                   + c * std(**kwargs)
               )
           ) | int


nikitin = norm(l=1) | mean_cascade.multi_mean()

nikitin_s = nikitin | abs | sigma3() | int

#
# mean_cascade.multi_mean()

seq_filters = [

    # SmartDict(
    #     name='windows',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='gray',
    #         linewidth=0.5,
    #     ),
    #     filter=DebugGridSWFilter(
    #         s=100,
    #         strict_windows=True,
    #         cs=False,
    #     ),
    # ),


    SmartDict(
        name='$F_{L_1} = |F_{t}|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='lightgray',
            marker='x',
            linewidth=3.0,
        ),
        filter=norm(l=1),
    ),

    SmartDict(
        name='$DTR_{300,2}$',
        plot_options=SmartDict(
            linestyle='-',
            color='red',
            # marker='x',
            linewidth=2.0,
        ),
        filter=norm(l=1) | dtr(s=300, d=2)
    ),
    #
    # SmartDict(
    #     name='$DTR2$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         #marker='x',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | delay(200) | dtr(s=300, d=1)
    # ),
    #
    #
    # SmartDict(
    #     name='$DTR3$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         #marker='x',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | delay(100) | dtr(s=300, d=2)
    # ),
    #
    #
    #
    # SmartDict(
    #     name='$\sum DTR$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='black',
    #         #marker='x',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | (
    #             dtr(s=301, d=2) + dtr(s=201, d=2) + dtr(s=100, d=2)
    #         # + (delay(200) | dtr(s=300, d=2))
    #     ) / 3
    # ),

    SmartDict(
        name='$S_{DTR} = \\frac{1}{k}\sum_{j=1}^{k} '
             'DTR_{i \cdot 25, 2} $',
        plot_options=SmartDict(
            linestyle='-',
            color='magenta',
            # marker='x',
            linewidth=2.0,
        ),
        filter=norm(l=1) | sum(
            [dtr(s=25 * i + 1) for i in xrange(1, 9)]
        ) / 8 | (sad | abs)
    ),

    SmartDict(
        name='$\\frac{1}{k}\sum_{j=1}^{k} Bills S_{DTR=}$',
        plot_options=SmartDict(
            linestyle=':',
            color='blue',
            # marker='x',
            linewidth=2.0,
        ),
        filter=norm(l=1) | sum(
            [dtr(s=25 * i + 1) for i in xrange(1, 9)]
        ) / 8 | (sad | abs) | sum(
            [sigma3(s=25 * i) for i in xrange(1, 9)]
        ) / 8
    ),

    # SmartDict(
    #     name='$DTR$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='orange',
    #         #marker='x',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | min_std_cascade.multi_dtr()
    # ),

    # SmartDict(
    #     name='$M_{25} = |\hat{\mu}_{25}(F_{L_1})|$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         #marker='x',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | mean(s=25, cs=True)
    # ),

    # SmartDict(
    #     name='$M_{50} = |\hat{\mu}_{50}(F_{L_1})|$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='orange',
    #         #marker='x',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | mean(s=50, cs=True)
    # ),

    #
    # SmartDict(
    #     name='$M_{100} = |\hat{\mu}_{100}(F_{L_1})|$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         #marker='x',
    #         color='red',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | mean(s=100, cs=True)
    # ),
    #
    # SmartDict(
    #     name='$M_{200} = |\hat{\mu}_{200}(F_{L_1})|$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | mean(s=200, cs=True)
    # ),
    #
    #
    #
    #
    # SmartDict(
    #     name='$|M_{100} - M_{50}| \\to_{\pm} 0$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='purple',
    #         linewidth=1.1,
    #     ),
    #     filter=norm(l=1) | median(s=25)
    #            | (mean(s=100, cs=True) - mean(s=50, cs=True))
    #            | sgn_changes | fabs * 1
    # ),
    #
    #
    # SmartDict(
    #     name='$|M_{200} - M_{50}| \\to_{\pm} 0$',
    #     plot_options=SmartDict(
    #         linestyle='--',
    #         color='blue',
    #         linewidth=1.2,
    #     ),
    #     filter=norm(l=1) | median(s=25)
    #            | (mean(s=200, cs=True) - mean(s=50, cs=True))
    #            | sgn_changes | fabs * 0.9
    # ),
    #
    #
    # SmartDict(
    #     name='$|M_{200} - M_{100}| \\to_{\pm} 0$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         marker='x',
    #         color='green',
    #         linewidth=1.3,
    #     ),
    #     filter=norm(l=1) | median(s=25)
    #            | (mean(s=200, cs=True) - mean(s=100, cs=True))
    #            | sgn_changes | fabs * 0.8
    # ),

    # SmartDict(
    #     name='$D_{t} = |F_{t} - F_{t-1}|_{L_1}$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='black',
    #         linewidth=2.0,
    #     ),
    #     filter=sad | abs | norm(l=1)
    # ),

    #
    # SmartDict(
    #     name='$D^{ffmpeg}_{t} = \min(D_t, D_t-D_{t-1})$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=2.0,
    #     ),
    #     filter=ffmpeglike
    # ),

    # SmartDict(
    #     name='$T_{const} = 0.08 \in (0; 1)$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='black',
    #         linewidth=2.0,
    #     ),
    #     filter=norm(l=1) | 0.08 ,
    # ),

    # SmartDict(
    #     name='$nikitin$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=3.0,
    #     ),
    #     filter= norm(l=1) | mean,
    # ),
    #
    #
    # SmartDict(
    #     name='$nikitin_s$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter= nikitin_s,
    # ),

    # SmartDict(
    #     name='$nikitin_e$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter= norm(l=1) | nikitin | extrema(s=99, x=1.1, order=50),
    # ),

    #
    # SmartDict(
    #     name='nikitin9',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter= nikitin9,
    # ),

    #
    #
    # SmartDict(
    #     name='nikitin61',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter= nikitin61,
    # ),

    #
    # SmartDict(
    #     name='std_e',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='orange',
    #         linewidth=1.0,
    #     ),
    #     filter= norm(l=1) | std_x | extrema(s=100, x=0.9),
    # ),

    #
    # SmartDict(
    #     name='$mean$',
    #     plot_options=SmartDict(
    #         linestyle='--',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | mean ,
    # ),
    #

    #
    # SmartDict(
    #     name='smooth',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='black',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | smooth ,
    # ),
    #
    #
    # SmartDict(
    #     name='$scale$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | smooth | extrema(s=100,x=1),
    # ),
    #
    # SmartDict(
    #     name='$scale min$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | smooth | extrema(s=100,x=1.1,case=min),
    # ),
    #
    #
    # SmartDict(
    #     name='$scale + d$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=delay(50) | norm(l=1) | smooth | extrema(s=100,x=0.5),
    # ),
    #
    # SmartDict(
    #     name='$scale+d min$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='orange',
    #         linewidth=1.0,
    #     ),
    #     filter=delay(50) | norm(l=1) | smooth | extrema(s=100,x=0.6,
    #                                                  case=min),
    # ),

    # SmartDict(
    #     name='$scale+d$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=delay(50) | norm(l=1) | mean  | extrema(s=100)
    # ),

    #
    # SmartDict(
    #      name='$corr$',
    #      plot_options=SmartDict(
    #          linestyle='-',
    #          color='red',
    #          linewidth=1.0,
    #      ),
    #      filter= mean(s=40) | norm(l=1),
    #  ),
    #
    # SmartDict(
    #      name='222',
    #      plot_options=SmartDict(
    #          linestyle='-',
    #          color='green',
    #          linewidth=1.0,
    #      ),
    #      filter= mean(s=40) | norm(l=1) | corr(s=10),
    #  ),

    # SmartDict(
    #     name='max',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | fmax,
    # ),
    #
    #
    # SmartDict(
    #     name='min',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | fmin,
    # ),
    #

    # SmartDict(
    #     name='mean',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | (mean(s=100) / std(s=100)) * 0.1,
    # ),

    # SmartDict(
    #     name='++',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | alpha_beta(
    #         alpha=0.1,
    #         beta=0.05,
    #         return_velocity = True,
    #     ),
    # ),

    # SmartDict(
    #     name='dct_re',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | dct_re(s=25),
    # ),

    #
    # SmartDict(
    #     name='zscore',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | zscore,
    # ),

    #
    # SmartDict(
    #     name='(original - mean) / std',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | (original - mean(s=50)) | fabs / std(s=40),
    # ),

    #
    # SmartDict(
    #     name='$R_{61} = DTR_{61,2}(F_i)$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1) | sad ,
    # ),
    #
    # SmartDict(
    #     name='$R_{47} = DTR_{47,1}(F_i)$',
    #     #offset=-1,
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1, window_delay=5,) | sad,
    # ),
    #
    #
    # SmartDict(
    #     name='$3 R_{47} = DTR_{47,1}(F_i)$',
    #     #offset=-1,
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1, window_delay=10) | sad,
    # ),
    #
    # SmartDict(
    #     name='$4 R_{47} = DTR_{47,1}(F_i)$',
    #     #offset=-1,
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='violet',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1, window_delay=15) | sad,
    # ),
    #
    # SmartDict(
    #     name='$5 R_{47} = DTR_{47,1}(F_i)$',
    #     #offset=-1,
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='orange',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1, window_delay=20) | sad,
    # ),

    #
    # SmartDict(
    #     name='sad',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter= (original - shift) | norm | fabs * 2,
    # ),
    #
    #
    # SmartDict(
    #     name='(original - mean(s=10)) | norm | fabs',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=(original - mean(s=50)) | norm | fabs * 2,
    # ),
    #
    # SmartDict(
    #     name='std',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=std(s=50) | norm | fabs * 2,
    # ),
    #
    #
    # SmartDict(
    #     name='dtr + | sad',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=norm
    #            | (dtr(s=47, d=1) | sad).i(dtr(s=61, d=2) | sad)
    #            | fabs | level(n=50)
    #            #| #adaptive_level(n=50, cm=1.1),
    # ),
]


class BaseEventSelector(BaseEventHandler):
    __logger = logging.getLogger(__name__)

    cumsum = 0

    plotter = BasePlotHandler()

    def plot(self, aevent_seq, plotter, filter_seq):

        """

        :param aevent_seq:
        :param plotter:
        :param filter_seq:
        """
        f_count = len(filter_seq)
        event_seq_tuple = itertools.tee(aevent_seq, f_count + 1)
        for filter_desc, event_seq in itertools.izip(
            filter_seq,
            event_seq_tuple[1:]
        ):
            offset = filter_desc.get('offset', 0)
            new_event_seq = filter_desc \
                .get('filter') \
                .filter_objects(event_seq)
            for event in new_event_seq:
                #
                # print (
                #     filter_desc.get('name'),
                #     event,
                #     event.time,
                #     event.feature
                # )
                filtered = event.feature
                time = event.time if event.time else 0
                plotter.add_data(
                    filter_desc.get('name'),
                    1.0 * (time - offset),
                    1.0 * filtered,
                    filter_desc.get('plot_style', ''),
                    **filter_desc.get('plot_options', {})
                )
        self.__logger.debug('plotter.plot_data() enter')
        plotter.plot_data()
        self.__logger.debug('plotter.plot_data() exit')
        return event_seq_tuple[0]

    def filter_events(self, event_seq, **kwargs):

        """
            Should be implemented
            :param event_seq: 
        """
        event_seq = self.limit_seq(event_seq, 0.0, 1.5)

        self.__logger.debug('plot enter')
        event_seq = self.plot(event_seq, self.plotter, seq_filters)
        self.__logger.debug('plot exit')

        #
        # filter = sad | fabs | norm | level(n=10)
        #
        # # event_seq = self.log_seq(event_seq, 'before')
        #
        # event_seq = filter.filter_objects(event_seq)
        #
        # event_seq = itertools.ifilter(lambda item: item.feature > 0.0,
        #                                    event_seq)
        #
        # event_seq = self.log_seq(event_seq, '-> {item} {item.feature}')
        #

        #
        # event_seq = self.log_seq(event_seq)
        #
        #
        # event_seq = itertools.ifilter(lambda x: x>0,
        #                                    event_seq)


        return event_seq
