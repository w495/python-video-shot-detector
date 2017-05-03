# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import os.path
import time

from shot_detector.detectors import SimpleDetector
from .base_service import BaseService


class BaseDetectorService(BaseService):

    def add_arguments(self, parser, **kwargs):
        parser = super(BaseDetectorService, self) \
            .add_arguments(parser, **kwargs)
        parser = self.add_input_arguments(parser, **kwargs)
        return parser

    def add_input_arguments(self, parser, **kwargs):

        parser.add_argument(
                '-i', '--input-uri',
                dest='raw_input_uri',
                default='{base}/{name}{ext}',
                metavar='URI',
                help='Name of the video file input or path '
                     'to the resource. You can use any string, '
                     'that can be accepted by input ffmpeg-parameter. '
                     'For example: '
                     '- `udp://localhost:1234`, '
                     '- `tcp://localhost:1234?listen`, '
                     '- `http://localhost:8090/live.flv`.'
                     '- `/mnt/raid/video.mp4`.'
                     'The `input-uri` can be formed as a pattern. '
                     'It is used to reduce the `input-uri` length.'
                     'For example, you have several files '
                     'in one directory. So you can specify '
                     'directory with `input-uri-base` in the config '
                     'and operate only with file names'
        )


        parser.add_argument(
            '--ib', '--input-uri-base',
            default='~/Videos',
            metavar='b',
            dest='input_uri_base',
            help='Value of {base} for `input-uri`'
        )

        parser.add_argument(
            '--in', '--input-uri-name',
            dest='input_uri_name',
            metavar='n',
            default='video',
            help='Value of {name} for `input-uri`'
        )

        parser.add_argument(
            '--ie', '--input-uri-ext',
            dest='input_uri_ext',
            metavar='e',
            default='.mp4',
            help='Value of {ext} for `input-uri`'
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
        options = super(BaseDetectorService, self) \
            .handle_options(options, **kwargs)
        options = self.handle_input_uri(options, **kwargs)
        return options



    def handle_input_uri(self, options, **kwargs):
        options = super(BaseDetectorService, self) \
            .handle_options(options, **kwargs)
        raw_input_uri = options.raw_input_uri
        if not raw_input_uri:
            raw_input_uri = ''

        options.input_uri = raw_input_uri .format(
                base=options.input_uri_base,
                name=options.input_uri_name,
                ext=options.input_uri_ext
        )

        home_dir = os.path.expanduser("~")
        options.input_uri = \
            options.input_uri.replace('~', home_dir)
        return options
