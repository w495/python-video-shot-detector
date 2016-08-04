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
        print(self.__class__)

        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()
        diff = delay(0) - shift
        ffmpeglike = FFMpegLikeTresholdSWFilter()
        swnorm = NormSWFilter(s=200)

        mean = MeanSWFilter()

        std = StdSWFilter()

        def sigma(c=3.0, s=1):
            return (delay(0) > (mean(s=s) + c * std(s=s))) | int

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
                name='$D_{t} '
                     '= \hat{\mu}_{25} + A \hat{\sigma}_{25}$',
                plot_options=SmartDict(
                    linestyle=':',
                    color='blue',
                    linewidth=1.0,
                ),
                filter=norm(l=1) | diff | modulus | sigma(s=25)
            ),
            SmartDict(
                name='$D_{t} '
                     '= \hat{\mu}_{50} + A \hat{\sigma}_{50}$',
                plot_options=SmartDict(
                    linestyle='--',
                    color='green',
                    linewidth=1.2,
                ),
                filter=norm(l=1) | diff | modulus | sigma(s=50) * 0.8
            ),
            SmartDict(
                name='$D_{t} '
                     '= \hat{\mu}_{100} + A \hat{\sigma}_{100}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='orange',
                    linewidth=1.8,
                ),
                filter=norm(l=1) | diff | modulus | sigma(s=100) * 0.6
            ),
            SmartDict(
                name='$D_{t} '
                     '= \hat{\mu}_{200} + A \hat{\sigma}_{200}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='red',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | diff | modulus | sigma(s=200) * 0.4
            ),

            # SmartDict(
            #     name='$D^{ffmpeg}_{t} = \min(D_t, D_t-D_{t-1})$',
            #     plot_options=SmartDict(
            #         linestyle='-',
            #         color='red',
            #         linewidth=2.0,
            #     ),
            #     filter=norm(l=1) | diff | modulus
            # ),

        ]
