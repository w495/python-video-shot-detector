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
        parser.add_argument(
            '--ff', '--first-frame',
            metavar='sec',
            dest='first_frame',
            type=int,
            default=0,
        )
        parser.add_argument(
            '--lf', '--last-frame',
            metavar='sec',
            dest='last_frame',
            type=int,
            default=60,
        )
        parser.add_argument(
            '--as', '--as-stream',
            default='no',
            dest='as_stream',
            type=yes_no,
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
            service_options=vars(options)
        )
