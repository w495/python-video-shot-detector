# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from .base_detector_service import BaseDetectorService

import os

from string import Template
from shot_detector.charts import Plotter

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

        group = parser.add_argument_group('plot arguments')


        group.add_argument(
            '-s',  '--plot-show',
            dest='plot_show',
            action='store_const',
            const=True,
            help='Value of {ext} for `input-uri`',
        )

        group.add_argument(
            '--px', '--plot-xlabel',
            metavar='text',
            dest='plot_xlabel',
            default='$L$',
            help='X-label for graphic',
        )

        group.add_argument(
            '--py', '--plot-ylabel',
            metavar='text',
            dest='plot_ylabel',
            default='$t$',
        )

        group.add_argument(
            '--pw', '--plot-width',
            metavar='cm',
            dest='plot_width',
            type=float,
            default=12.0,
        )

        group.add_argument(
            '--ph', '--plot-height',
            metavar='cm',
            dest='plot_height',
            type=float,
            default=9.0,
        )

        group.add_argument(
            '--pff', '--plot-font-family',
            metavar='font',
            dest='plot_font_family',
            default='DejaVu Sans',
        )

        group.add_argument(
            '--pfs', '--plot-font-size',
            metavar='pt',
            type=int,
            dest='plot_font_size',
            default=14,
        )

        group.add_argument(
            '--psf', '--plot-save-format',
            dest='plot_save_format',
            default='pdf',
            choices=['pdf', 'png']
        )

        group.add_argument(
            '--psr', '--plot-save-root',
            default='~/Documents/Charts',
            metavar='path',
            dest='plot_save_root',
        )

        group.add_argument(
            '--psd', '--plot-save-dir',
            default="${root}/"
                    "Researched/"
                    "${chart}/",
            metavar='path',
            dest='plot_save_dir',
        )

        group.add_argument(
            '--psn', '--plot-save-name',
            default="${root}/"
                    "Autosaved/"
                    "${chart}/"
                    "${name}-${ff}-${lf}.${ext}",
            metavar='file-name.pdf',
            dest='plot_save_name',
        )



        return parser

    def handle_options(self, options, **kwargs):
        """

        :param options:
        :param kwargs:
        :return:
        """
        options = super(PlotService, self).handle_options(options, **kwargs)
        options = self.handle_plot_mode(options, **kwargs)
        return options



    def handle_plot_mode(self, options, **kwargs):

        plotter_mode = set()

        if options.plot_show is not None:
            plotter_mode.add(
                Plotter.Mode.SHOW_PLOT
            )


        if options.plot_save_name is not None:
            plotter_mode.add(
                Plotter.Mode.SAVE_PLOT
            )


        input_uri_tail = os.path.basename(options.input_uri)
        input_uri_name, _ = os.path.splitext(input_uri_tail)

        home_dir = os.path.expanduser("~")
        template_params = dict(
            home=home_dir,
            name=input_uri_name,
            chart="${chart}",
            ff=options.first_frame,
            lf=options.last_frame,
            ext=options.plot_save_format
        )

        plot_root_template = Template(options.plot_save_root)
        plot_save_root = plot_root_template.safe_substitute(
            **template_params
        )
        plot_save_root = plot_save_root.replace('~', home_dir)
        options.plot_save_root  = plot_save_root

        plot_dir_template = Template(options.plot_save_dir)
        plot_save_dir = plot_dir_template.safe_substitute(
            root=plot_save_root,
            **template_params
        )
        plot_save_dir = plot_save_dir.replace('~', home_dir)
        options.plot_save_dir  = plot_save_dir

        plot_save_template = Template(options.plot_save_name)
        plot_save_name = plot_save_template.safe_substitute(
            root=plot_save_root,
            dir=plot_save_dir,
            **template_params
        )
        plot_save_name = plot_save_name.replace('~', home_dir)
        options.plot_save_name  = plot_save_name

        plotter = Plotter(
            xlabel=options.plot_xlabel,
            ylabel=options.plot_ylabel,
            width=options.plot_width,
            height=options.plot_height,
            font_family=options.plot_font_family,
            font_size=options.plot_font_size,
            save_dir=options.plot_save_dir,
            save_format=options.plot_save_format,
            save_name=plot_save_name,
            display_mode=plotter_mode,
        )

        options.plotter = plotter
        return options
