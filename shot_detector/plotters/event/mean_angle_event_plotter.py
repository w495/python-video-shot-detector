# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    MeanSWFilter,
    NormFilter,
    SignChangeFilter,
    NormSWFilter,
)
from shot_detector.utils.collections import SmartDict
from .base_event_plotter import BaseEventPlotter


class MeanAngleEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        print(self.__class__)

        swnorm = NormSWFilter(s=200)

        norm = NormFilter()

        sgn_changes = SignChangeFilter(use_angle=True)

        mean = MeanSWFilter(window_size=25)

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
                    # marker='x',
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
                    # marker='x',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | mean(s=200)
            ),

            SmartDict(
                name='$|M_{100} - M_{50}| \\to_{\pm} 0$',
                plot_options=SmartDict(
                    linestyle='-',
                    marker='x',
                    color='purple',
                    linewidth=1.1,
                ),
                filter=norm(l=1) | mean(s=50) - mean(s=200)
                       | sgn_changes | swnorm
            ),

        ]
