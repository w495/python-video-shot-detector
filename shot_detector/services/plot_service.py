# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import os
from string import Template

from shot_detector.charts import Plotter
from .base_detector_service import BaseDetectorService


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

        group = parser.add_argument_group('Plot Arguments')

        group.add_argument(
            '-s', '--plot-show',
            dest='plot_show',
            action='store_const',
            const=True,
            help='Value of {ext} for `input-uri`',
        )

        label_group = group.add_argument_group(
            title='Plot Label Arguments',
            description='What for'

        )

        label_group.add_argument(
            '+px', '--plot-xlabel',
            metavar='text',
            dest='plot_xlabel',
            default='$L$',
            help='X-label for graphic',
        )

        label_group.add_argument(
            '+py', '--plot-ylabel',
            metavar='text',
            dest='plot_ylabel',
            default='$t$',
        )


        size_group = group.add_argument_group('Plot Size Arguments')

        size_group.add_argument(
            '+pw', '--plot-width',
            metavar='cm',
            dest='plot_width',
            type=float,
            default=12.0,
        )

        size_group.add_argument(
            '+ph', '--plot-height',
            metavar='cm',
            dest='plot_height',
            type=float,
            default=9.0,
        )


        font_group = group.add_argument_group('Plot Font Arguments')

        font_group.add_argument(
            '+pF', '--plot-font-family',
            metavar='font',
            dest='plot_font_family',
            default='DejaVu Sans',
        )

        font_group.add_argument(
            '+pS', '--plot-font-size',
            metavar='pt',
            type=int,
            dest='plot_font_size',
            default=14,
        )


        save_group = group.add_argument_group('Plot Save Arguments')

        save_group.add_argument(
            '+pR', '--plot-save-root',
            default='~/Documents/Charts',
            metavar='path',
            dest='plot_save_root',
        )

        save_group.add_argument(
            '+pD', '--plot-save-dir',
            default="${root}/"
                    "Researched/"
                    "${chart}/",
            metavar='path',
            dest='plot_save_dir',
        )

        save_group.add_argument(
            '+pn', '--plot-save-name',
            default="${root}/"
                    "Auto-saved/"
                    "${chart}/"
                    "${name}-${ff}-${lf}.${ext}",
            metavar='file-name.pdf',
            dest='plot_save_name',
        )

        save_group.add_argument(
            '+pf', '--plot-save-format',
            dest='plot_save_format',
            default='pdf',
            choices=['pdf', 'png']
        )

        return parser

    def handle_options(self, options, **kwargs):
        """

        :param options:
        :param kwargs:
        :return:
        """
        options = super(PlotService, self).handle_options(options,
                                                          **kwargs)
        options = self.handle_plot_mode(options, **kwargs)
        return options

    @staticmethod
    def handle_plot_mode(options, **_):
        """
        
        :param options:  
        :return: 
        """

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
        options.plot_save_root = plot_save_root

        plot_dir_template = Template(options.plot_save_dir)
        plot_save_dir = plot_dir_template.safe_substitute(
            root=plot_save_root,
            **template_params
        )
        plot_save_dir = plot_save_dir.replace('~', home_dir)
        options.plot_save_dir = plot_save_dir

        plot_save_template = Template(options.plot_save_name)
        plot_save_name = plot_save_template.safe_substitute(
            root=plot_save_root,
            dir=plot_save_dir,
            **template_params
        )
        plot_save_name = plot_save_name.replace('~', home_dir)
        options.plot_save_name = plot_save_name


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
