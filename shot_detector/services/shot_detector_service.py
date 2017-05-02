# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import time

from shot_detector.detectors import SimpleDetector
from .base_detector_service import BaseDetectorService
from .plot_service import PlotService

from shot_detector.utils.common import yes_no

class ShotDetectorPlotService(PlotService, BaseDetectorService):
    """
    Simple Shot Detector Service.

    """

    def add_arguments(self, parser, **kwargs):
        parser = super(ShotDetectorPlotService, self) \
            .add_arguments(parser, **kwargs)
        parser = self.add_video_arguments(parser, **kwargs)
        parser = self.add_plot_arguments(parser, **kwargs)
        return parser

    def add_video_arguments(self, parser, **kwargs):

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

    def run(self, *kwargs):
        options = self.options

        detector = SimpleDetector()

        t1 = time.time()

        detector.detect(
            input_uri=options.input_uri,
            format=options.format,
            service_options=vars(options)
        )

        t2 = time.time()
        print(t2 - t1)
