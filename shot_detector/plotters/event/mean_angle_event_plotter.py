# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    MeanSWFilter,
    DelayFilter,
    ShiftSWFilter,
    NormFilter,
    JoinFilter,
    StdSWFilter,
    ConditionFilter,
    ModulusFilter,
    AngleChangeFilter,
    SgnChangeFilter,
    LevelSWFilter,
    NormSWFilter,
)
from shot_detector.utils.collections import SmartDict
from .base_event_plotter import BaseEventPlotter


class MeanAngleEventPlotter(BaseEventPlotter):

    __logger = logging.getLogger(__name__)

    def seq_filters(self):

        join = JoinFilter()

        delay = DelayFilter()

        norm = NormFilter()

        modulus = ModulusFilter()

        shift = ShiftSWFilter()

        diff = delay(0) - shift

        level = LevelSWFilter(
            s=5,
            level_number=10000,
            #global_max=1.0,
            #global_min=0.0,
        )


        norm = NormFilter()
        fabs = ModulusFilter()
        sgn_changes = SgnChangeFilter()
        angle_changes = AngleChangeFilter()
        mean = MeanSWFilter(window_size=25)
        std = StdSWFilter(window_size=25)


        cond = ConditionFilter()

        def bill(c=1.0,s=5):
            return (delay(0) > (mean(s=s) + c*std(s=s))) | int

        return [
            SmartDict(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='lightgray',
                    linewidth=3.0,
                ),
                filter=norm(l=1),
            ),

            SmartDict(
                name='$M_{50} = |\hat{\mu}_{50}(F_{L_1})|$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='orange',
                    #marker='x',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | mean(s=50)
            ),

            SmartDict(
                name='$M_{100} = |\hat{\mu}_{100}(F_{L_1})|$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='red',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | mean(s=100)
            ),

            SmartDict(
                name='$M_{200} = |\hat{\mu}_{200}(F_{L_1})|$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='blue',
                    #marker='x',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | mean(s=200)
            ),

            # SmartDict(
            #     name='$|M_ddd{100} - M_{50}| \\to_{\pm} 0$',
            #     plot_options=SmartDict(
            #         linestyle='-',
            #         color='green',
            #         marker='x',
            #         linewidth=1.1,
            #     ),
            #     filter=norm(l=1)
            #            | (mean(s=50) - mean(s=200))
            # ),

            SmartDict(
                name='$|M_{100} - M_{50}| \\to_{\pm} 0$',
                plot_options=SmartDict(
                    linestyle='-',
                    marker='x',
                    color='purple',
                    linewidth=1.1,
                ),
                filter= norm(l=1) | join(mean(s=50), mean(s=200))
                        | angle_changes | NormSWFilter(s=200)
            ),

        ]
