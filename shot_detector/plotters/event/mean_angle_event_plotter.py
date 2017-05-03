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
from shot_detector.plotters.event.base import (
    BaseEventPlotter,
    FilterDescription,
    PlotOptions
)


class MeanAngleEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        print(self.__class__)

        swnorm = NormSWFilter(s=200)

        norm = NormFilter()

        sgn_changes = SignChangeFilter(use_angle=True)

        mean = MeanSWFilter(window_size=25)

        return [
            FilterDescription(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='lightgray',
                    width=3.0,
                ),
                filter=norm(l=1),
            ),

            FilterDescription(
                name='$M_{50} = |\hat{\mu}_{50}(F_{L_1})|$',
                plot_options=PlotOptions(
                    style='-',
                    color='orange',
                    # marker='x',
                    width=2.0,
                ),
                filter=norm(l=1) | mean(s=50)
            ),

            FilterDescription(
                name='$M_{100} = |\hat{\mu}_{100}(F_{L_1})|$',
                plot_options=PlotOptions(
                    style='-',
                    color='red',
                    width=2.0,
                ),
                filter=norm(l=1) | mean(s=100)
            ),

            FilterDescription(
                name='$M_{200} = |\hat{\mu}_{200}(F_{L_1})|$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    # marker='x',
                    width=2.0,
                ),
                filter=norm(l=1) | mean(s=200)
            ),

            FilterDescription(
                name='$|M_{100} - M_{50}| \\to_{\pm} 0$',
                plot_options=PlotOptions(
                    style='-',
                    marker='x',
                    color='purple',
                    width=1.1,
                ),
                filter=norm(l=1) | mean(s=50) - mean(s=200)
                       | sgn_changes | swnorm
            ),

        ]
