# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    FFMpegLikeTresholdSWFilter,
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    MeanSWFilter,
    StdSWFilter,
    ModulusFilter,
    NormSWFilter,
)
from shot_detector.utils.collections import SmartDict
from .base_event_plotter import BaseEventPlotter


class SigmaThresholdEventPlotter(BaseEventPlotter):

    __logger = logging.getLogger(__name__)

    def seq_filters(self):

        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()
        diff = delay(0) - shift
        ffmpeglike = FFMpegLikeTresholdSWFilter()
        swnorm = NormSWFilter(s=200)


        mean = MeanSWFilter()

        std = StdSWFilter()

        def sigma(c=3.0,s=1):
            return (delay(0) > (mean(s=s) + c*std(s=s))) | int


        return [
            SmartDict(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='gray',
                    linewidth=3.0,
                ),
                filter=norm(l=1),
            ),


          SmartDict(
                name='$D^{ffmpeg}_{\,200,t} '
                     '= swnorm_{\,200} D^{ffmpeg}_{t}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='orange',
                    linewidth=1.0,
                ),
                filter=ffmpeglike | sigma(s=200)
            ),


            SmartDict(
                name='$D^{ffmpeg}_{t} = \min(D_t, D_t-D_{t-1})$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='red',
                    linewidth=2.0,
                ),
                filter=ffmpeglike
            ),






            SmartDict(
                name='$T_{const} = 0.8 \in (0; 1)$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='black',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | 0.8 ,
            ),
        ]
