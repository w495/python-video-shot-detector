# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import os.path
import time

from shot_detector.detectors import SimpleDetector
from .base_service import BaseService


class ShotDetectorService(BaseService):
    """

    sdsd
    sdsd.



    """

    def add_arguments(self, parser, **kwargs):
        parser = super(ShotDetectorService, self) \
            .add_arguments(parser, **kwargs)

        parser.add_argument(
                '-i', '--input-uri',
                dest='raw_input_uri',
                default='~/Videos/video.mp4',
                metavar='URI',
                help='Name of the video file input or path '
                     'to the resource. You can use any string, '
                     'that can be accepted by input ffmpeg-parameter. '
                     'For example: '
                     '- `udp://localhost:1234`, '
                     '- `tcp://localhost:1234?listen`, '
                     '- `http://localhost:8090/live.flv`.'
                     '- `/mnt/raid/video.mp4`.'
        )

        parser.add_argument(
                '--ip', '--input-pattern',
                dest='input_pattern',
                default='{uri}',
                metavar='{URI}',
                help='Pattern for `input-uri`. '
                     'It is used to reduce the `input-uri` length.'
                     'For example, you have several files '
                     'in one directory. So you can specify you '
                     'directory in the config and operate '
                     'only with file names.'
        )

        parser.add_argument(
                '-f', '--format',
                metavar='fmt',
                help='Force input format. The format is normally '
                     'auto detected for input files so this option '
                     'is not needed in most cases. Use it for '
                     'hardware devices.'
        )

        return parser

    def handle_options(self, options, **kwargs):
        options = super(ShotDetectorService, self) \
            .handle_options(options, **kwargs)
        raw_input_uri = options.raw_input_uri
        if not raw_input_uri:
            raw_input_uri = ''
        input_pattern = options.input_pattern
        if not input_pattern:
            input_pattern = '{input_uri}'

        options.input_uri = input_pattern.format(
                uri=raw_input_uri,
        )
        home_dir = os.path.expanduser("~")
        options.input_uri = \
            options.input_uri.replace('~', home_dir)
        return options

    def run(self, *kwargs):
        options = self.options

        detector = SimpleDetector()

        t1 = time.time()

        detector.detect(
                input_uri=options.input_uri,
                format=options.format
        )

        t2 = time.time()
        print(t2 - t1)
