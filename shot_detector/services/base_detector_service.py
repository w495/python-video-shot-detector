# -*- coding: utf8 -*-
"""
    ...
"""

from __future__ import absolute_import, division, print_function

import os.path
from string import Template

from .base_service import BaseService


class BaseDetectorService(BaseService):
    """
        ...
    """

    def add_arguments(self, parser, **kwargs):
        """
        
        :param parser: 
        :param kwargs: 
        :return: 
        """
        parser = super(BaseDetectorService, self) \
            .add_arguments(parser, **kwargs)
        parser = self.add_input_arguments(parser, **kwargs)
        return parser

    # noinspection PyUnusedLocal
    @staticmethod
    def add_input_arguments(parser, **kwargs):
        """
        
        :param parser: 
        :param kwargs: 
        :return: 
        """

        basic_group = parser.add_argument_group(
            'Video Input Arguments'
        )
        basic_group.add_argument(
            '-i', '--input-uri',
            dest='raw_input_uri',
            default='${base}/${name}${ext}',
            metavar='URI',
            help='Name of the video file input or path '
                 'to the resource. You can use any string, '
                 'that can be accepted by input ffmpeg-parameter.\\'
                 'For~example:\\'
                 '- [udp://localhost:1234],\\'
                 '- [tcp://localhost:1234?listen],\\'
                 '- [http://localhost:8090/live.flv].\\'
                 '- [/mnt/raid/video.mp4].\\'
                 'The `input-uri` can be formed as a pattern. '
                 'It is used to reduce the `input-uri` length. '
                 'For example, you have several files '
                 'in one directory. So you can specify '
                 'directory with `input-uri-base` in the~config '
                 'and operate only with file names'
        )
        basic_group.add_argument(
            '-f', '--format',
            metavar='fmt',
            help='Force input format. The format is normally '
                 'auto detected for input files so this option '
                 'is not needed in most cases. Use it for '
                 'hardware devices.'
        )

        advanced_group = basic_group.add_argument_group(
            'Advanced Video input arguments'
        )
        advanced_group.add_argument(
            '+ib', '--input-uri-base',
            default='${home}/Videos',
            metavar='b',
            dest='input_uri_base',
            help='Value of base for input-uri. '
                 'The `input-uri` can be formed as a pattern. '
                 'It is used to reduce the `input-uri` length.'
                 'For example, you have several files '
                 'in one directory. So you can specify '
                 'directory with `input-uri-base` in the config '
                 'and operate only with file names'
        )

        advanced_group.add_argument(
            '+in', '--input-uri-name',
            dest='input_uri_name',
            metavar='n',
            default='video',
            help='Value of {name} for `input-uri`'
        )

        advanced_group.add_argument(
            '+ie', '--input-uri-ext',
            dest='input_uri_ext',
            metavar='e',
            default='.mp4',
            help='Value of {ext} for `input-uri`'
        )


        return parser

    def handle_options(self, options, **kwargs):
        """
        
        :param options: 
        :param kwargs: 
        :return: 
        """
        options = super(BaseDetectorService, self) \
            .handle_options(options, **kwargs)
        options = self.handle_input_uri(options, **kwargs)
        return options

    def handle_input_uri(self, options, **kwargs):
        """
        
        :param options: 
        :param kwargs: 
        :return: 
        """
        options = super(BaseDetectorService, self) \
            .handle_options(options, **kwargs)
        raw_input_uri = options.raw_input_uri
        if not raw_input_uri:
            raw_input_uri = ''

        home_dir = os.path.expanduser("~")
        input_uri_base_template = Template(options.input_uri_base)
        input_uri_base = input_uri_base_template.substitute(
            home=home_dir,
        )
        input_uri_base = input_uri_base.replace('~', home_dir)
        options.input_uri_base = input_uri_base

        input_uri_template = Template(raw_input_uri)
        input_uri = input_uri_template.substitute(
            home=home_dir,
            base=options.input_uri_base,
            name=options.input_uri_name,
            ext=options.input_uri_ext
        )
        input_uri = input_uri.replace('~', home_dir)
        options.input_uri = input_uri

        return options
