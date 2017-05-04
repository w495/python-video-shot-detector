# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

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
    MeanSWFilter,
    StdSWFilter,
    ModulusFilter,
    NormSWFilter,
)
from shot_detector.plotters.event.base import (
    BaseEventPlotter,
    FilterDescription,
    PlotOptions
)


class SigmaThresholdEventPlotter(BaseEventPlotter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        """
        
        :return: 
        """
        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()
        diff = delay(0) - shift
        # noinspection PyUnusedLocal
        ffmpeg_like = FFMpegLikeThresholdSWFilter()
        # noinspection PyUnusedLocal
        sw_norm = NormSWFilter(s=200)

        mean = MeanSWFilter()

        std = StdSWFilter()

        def sigma(c=3.0, s=1):
            """
            
            :param c: 
            :param s: 
            :return: 
            """
            # noinspection PyTypeChecker
            return (delay(0) > (mean(s=s) + c * std(s=s))) | int

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

            FilterDescription(
                name='$D_{t} '
                     '= \hat{\mu}_{25} + A \hat{\sigma}_{25}$',
                plot_options=PlotOptions(
                    style=':',
                    color='blue',
                    width=1.0,
                ),
                formula=norm(l=1) | diff | modulus | sigma(s=25)
            ),
            FilterDescription(
                name='$D_{t} '
                     '= \hat{\mu}_{50} + A \hat{\sigma}_{50}$',
                plot_options=PlotOptions(
                    style='--',
                    color='green',
                    width=1.2,
                ),
                formula=norm(l=1) | diff | modulus | sigma(s=50) * 0.8
            ),
            FilterDescription(
                name='$D_{t} '
                     '= \hat{\mu}_{100} + A \hat{\sigma}_{100}$',
                plot_options=PlotOptions(
                    style='-',
                    color='orange',
                    width=1.8,
                ),
                formula=norm(l=1) | diff | modulus | sigma(s=100) * 0.6
            ),
            FilterDescription(
                name='$D_{t} '
                     '= \hat{\mu}_{200} + A \hat{\sigma}_{200}$',
                plot_options=PlotOptions(
                    style='-',
                    color='red',
                    width=2.0,
                ),
                formula=norm(l=1) | diff | modulus | sigma(s=200) * 0.4
            ),

            # FilterDescription(
            #     name='$D^{ffmpeg}_{t} = \min(D_t, D_t-D_{t-1})$',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='red',
            #         width=2.0,
            #     ),
            #     filter=norm(l=1) | diff | modulus
            # ),

        ]
