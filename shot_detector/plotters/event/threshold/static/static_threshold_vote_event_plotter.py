# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    FFMpegLikeThresholdSWFilter,
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    ModulusFilter,
    NormSWFilter,
)
from shot_detector.plotters.event.base import (
    BaseEventPlotter,
    FilterDescription,
    PlotOptions
)


class StaticThresholdVoteEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        self.__logger.info("--")

        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()
        diff = delay(0) - shift
        # noinspection PyUnusedLocal
        ffmpeg_like = FFMpegLikeThresholdSWFilter()
        swnorm = NormSWFilter(s=200)

        return [
            FilterDescription(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='gray',
                    width=3.0,
                ),
                formula=norm(l=1),
            ),

            # FilterDescription(
            #     name='$+ D^{ffmpeg}_{\,200,t} '
            #          '= swnorm_{\,200} D^{ffmpeg}_{t}$',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='orange',
            #         width=1.0,
            #     ),
            #     filter=norm(l=1) | diff | sum(
            #         swnorm(s=i*50) for i in range(1, 9)
            #     ) / 8
            # ),

            FilterDescription(
                name='$+ D^{ffmpeg}_{\,50,t} '
                     '= swnorm_{\,200} D^{ffmpeg}_{t}$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    width=1.0,
                ),
                formula=norm(l=1) | diff | modulus | swnorm(s=50)
            ),

            FilterDescription(
                name='$+ D^{ffmpeg}_{\,100,t} '
                     '= swnorm_{\,200} D^{ffmpeg}_{t}$',
                plot_options=PlotOptions(
                    style='-',
                    color='orange',
                    width=1.0,
                ),
                formula=norm(l=1) | diff | modulus | swnorm(s=100)
            ),

            FilterDescription(
                name='$+ D^{ffmpeg}_{\,200,t} '
                     '= swnorm_{\,200} D^{ffmpeg}_{t}$',
                plot_options=PlotOptions(
                    style='-',
                    color='red',
                    width=1.0,
                ),
                formula=norm(l=1) | diff | modulus | swnorm(s=200)
            ),

            #
            # FilterDescription(
            #     name='$D^{ffmpeg}_{t} = \min(D_t, D_t-D_{t-1})$',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='red',
            #         width=2.0,
            #     ),
            #     filter=ffmpeg_like
            # ),
            #


            FilterDescription(
                name='$T_{const} = 0.8 \in (0; 1)$',
                plot_options=PlotOptions(
                    style='-',
                    color='black',
                    width=2.0,
                ),
                formula=norm(l=1) | 0.8,
            ),
        ]
