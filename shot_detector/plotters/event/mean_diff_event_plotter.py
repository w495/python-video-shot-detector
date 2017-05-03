# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    MeanSWFilter,
    NormFilter,
    ModulusFilter,
    SignChangeFilter
)
from shot_detector.plotters.event.base import (
    BaseEventPlotter,
    FilterDescription,
    PlotOptions
)


class MeanDiffEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        print(self.__class__)

        norm = NormFilter()
        fabs = ModulusFilter()
        sgn_changes = SignChangeFilter()
        mean = MeanSWFilter(window_size=25)

        # noinspection PyTypeChecker
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
                    width=2.0,
                ),
                filter=norm(l=1) | mean(s=200)
            ),

            FilterDescription(
                name='$|M_{100} - M_{50}| \\to_{\pm} 0$',
                plot_options=PlotOptions(
                    style=':',
                    color='purple',
                    width=1.1,
                ),
                filter=norm(l=1)
                       | (mean(s=100) - mean(s=50))
                       | sgn_changes | fabs * 1
            ),

            FilterDescription(
                name='$|M_{200} - M_{50}| \\to_{\pm} 0$',
                plot_options=PlotOptions(
                    style='--',
                    color='blue',
                    width=1.2,
                ),
                filter=norm(l=1)
                       | (mean(s=200) - mean(s=50))
                       | sgn_changes | fabs * 0.9
            ),

            FilterDescription(
                name='$|M_{200} - M_{100}| \\to_{\pm} 0$',
                plot_options=PlotOptions(
                    style='-',
                    marker='x',
                    color='green',
                    width=1.3,
                ),
                filter=norm(l=1)
                       | (mean(s=200) - mean(s=100))
                       | sgn_changes | fabs * 0.8
            )
        ]
