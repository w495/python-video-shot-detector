# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from .base_detector_service import BaseDetectorService



from shot_detector.utils.common import yes_no

class PlotService(BaseDetectorService):
    """
    Simple Shot Detector Service

    """

    @staticmethod
    def add_plot_arguments(parser, **_):
        """
        
        :param parser: 
        :param _: 
        :return: 
        """

        parser.add_argument(
            'aaa',
            default='$L$',
            help='X-label for graphic',
        )


        parser.add_argument(
            'bbb',
            default='$L$',
            help='X-label for graphic',
        )


        parser.add_argument(
            'ccc',
            default='$L$',
            choices=[1,2,3],
            help='X-label for graphic',
        )

        parser.add_argument(
            '--px', '--plot-xlabel',
            metavar='text',
            dest='plot_xlabel',
            default='$L$',
            help='X-label for graphic',
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
            '--pff', '--plot-font-family',
            metavar='font',
            dest='plot_font_family',
            default='DejaVu Sans',
        )

        parser.add_argument(
            '--pfs', '--plot-font-size',
            metavar='pt',
            type=int,
            dest='plot_font_size',
            default=14,
        )

        parser.add_argument(
            '--psf', '--plot-save-format',
            dest='plot_save_format',
            default='pdf',
            choices=['pdf', 'png']
        )

        parser.add_argument(
            '--psd', '--plot-save-dir',
            default='.',
            metavar='path',
            dest='plot_save_dir',
        )

        parser.add_argument(
            '--psn', '--plot-save-name',
            default=None,
            metavar='file-name.pdf',
            dest='plot_save_name',
        )


        parser.add_argument(
            '--pd', '--plot-display',
            default='no',
            dest='__as_stream',
            help='Value of {ext} for `input-uri`',
            type=yes_no,
        )

        return parser
