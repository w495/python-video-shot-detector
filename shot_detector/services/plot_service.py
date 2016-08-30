# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import time

from shot_detector.detectors import SimpleDetector
from .base_detector_service import BaseDetectorService


class PlotService(BaseDetectorService):
    """
    Simple Shot Detector Service

    """

    def add_plot_arguments(self, parser, **kwargs):


        parser.add_argument(
                '--px', '--plot-xlabel',
                metavar='text',
                dest='plot_xlabel',
                default='$L$',
        )

        parser.add_argument(
                '--py', '--plot-ylabel',
                metavar='text',
                dest='plot_ylabel',
                default='$t$',
        )

        parser.add_argument(
                '--pw', '--plot-width',
                metavar='cm',
                dest='plot_width',
                type=float,
                default=12.0,
        )

        parser.add_argument(
                '--ph', '--plot-height',
                metavar='cm',
                dest='plot_height',
                type=float,
                default=9.0,
        )

        parser.add_argument(
                '--pf', '--plot-format',
                dest='plot_format',
                default='pdf',
                choices=['pdf', 'png']
        )

        # parser.add_argument(
        #         '--pff', '--plot-font-family',
        #         metavar='font',
        #         dest='plot_font_family',
        #         default='DejaVu Sans',
        # )

        parser.add_argument(
                '--pfs', '--plot-font-size',
                metavar='pt',
                type=int,
                dest='plot_font_size',
                default=14,
        )

        parser.add_argument(
                '--psd', '--plot-save-dir',
                default='.',
                metavar='path',
                dest='plot_save_dir',
        )

        return parser


