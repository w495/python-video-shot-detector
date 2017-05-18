# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.detectors import SimpleDetector
from shot_detector.utils.common import yes_no
from shot_detector.utils.log_meta import log_method_call_with
from .base_detector_service import BaseDetectorService
from .plot_service import PlotService



from shot_detector.charts import Plotter

class ShotDetectorPlotService(PlotService, BaseDetectorService):
    """
    Simple Shot Detector Service.

    """

    def add_arguments(self, parser, **kwargs):
        """
        
        :param parser: 
        :param kwargs: 
        :return: 
        """
        parser = super(ShotDetectorPlotService, self) \
            .add_arguments(parser, **kwargs)
        parser = self.add_video_arguments(parser, **kwargs)
        parser = self.add_plot_arguments(parser, **kwargs)
        return parser

    @staticmethod
    def add_video_arguments(parser, **_):
        """
        
        :param parser: 
        :param _: 
        :return: 
        """

        group = parser.add_argument_group('video handler arguments')

        group.add_argument(
            '--ff', '--video-first-frame',
            metavar='sec',
            dest='first_frame',
            type=int,
            default=0,
        )
        group.add_argument(
            '--lf', '--video-last-frame',
            metavar='sec',
            dest='last_frame',
            type=int,
            default=60,
        )
        group.add_argument(
            '--as', '--as-stream',
            default='no',
            dest='as_stream',
            choices={'yes','no'}
        )
        return parser

    @log_method_call_with(
        level=logging.WARN,
        logger=logging.getLogger(__name__)
    )
    def run(self, *kwargs):
        """
        
        :param kwargs: 
        :return: 
        """
        options = self.options
        detector = SimpleDetector()
        detector.detect(
            input_uri=options.input_uri,
            format=options.format,
            first_frame=options.first_frame,
            last_frame=options.last_frame,
            as_stream=options.as_stream,
            plotter=options.plotter,
            service_options=options
        )
