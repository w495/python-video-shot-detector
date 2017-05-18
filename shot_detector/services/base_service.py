# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import argparse
import logging
import platform
import re

import six

from shot_detector.utils import ConfigArgParser, LogMeta

from shot_detector.utils import ColoredHelpFormatter


from shot_detector.utils.collections import ObjDict

class ServiceNamespace(ObjDict):
    log_base = None



class BaseService(six.with_metaclass(LogMeta)):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    DEFAULT_VERSION = '0.0.8'

    DEFAULT_LOG_DIR_PATTERN = '/var/log/{service_name}'

    DEFAULT_GLOBAL_CONFIG_DIR = '/etc'
    DEFAULT_LOCAL_CONFIG_DIR = 'config'

    DEFAULT_CONFIG_EXTENSIONS = {
        '.ini',
        '.cnf',
        '.yaml',
        '.conf'
    }

    DEFAULT_CONFIG_PATHS = [
        "{global_config_base}/{service_name}{extension}",
        "{local_config_base}/{service_name}{extension}",
        "{local_config_base}/default{extension}",
        "{service_name}{extension}",
        "config{extension}",
    ]

    DEFAULT_SERVICE_NAME = None

    def __init__(self, parser=None, **kwargs):
        """
        
        :param parser: 
        :param kwargs: 
        """
        if not parser:
            parser = self.get_parser(**kwargs)
        parser = self.add_arguments(parser, **kwargs)
        options = self.parse_args(parser=parser)
        self.options = self.handle_options(options=options)
        self.options.kwargs = kwargs

    def parse_args(self, parser, namespace=None, **_):
        """
        
        :param parser: 
        :param namespace: 
        :param _: 
        :return: 
        """

        if namespace is None:
            namespace = ServiceNamespace(
                service_class=type(self)
            )
        options = parser.parse_args(
            namespace=namespace
        )
        return options


    def get_parser(self, **kwargs):
        """
        
        :param kwargs: 
        :return: 
        """
        parser = ConfigArgParser(
            version=self.get_version(**kwargs),
            ignore_unknown_config_file_keys=True,
            # add_config_file_help=False,
            args_for_setting_config_path=['-c', '--config'],
            default_config_files=list(
                self.config_file_names(**kwargs)
            ),
            formatter_class=ColoredHelpFormatter,
            #formatter_class=argparse.ArgumentDefaultsHelpFormatter,

            description=self.get_description(**kwargs),
            epilog=self.get_epilog(**kwargs),
            prefix_chars='-+?',
            conflict_handler='resolve',
        )
        return parser

    def add_arguments(self, parser, **kwargs):
        """
        
        :param parser: 
        :param kwargs: 
        :return: 
        """


        group = parser.add_argument_group('common arguments')

        group.add_argument(
            '-v', '--version',
            action='version',
            version=self.get_version(**kwargs),
            help='Shows the version'
        )

        group.add_argument(
            '--log-base',
            default=self.get_log_base(**kwargs),
            metavar='path',
            help='Path to directory with logs. '
                 'Note: this script has several log files. '
        )

        return parser

    def handle_options(self, options, **kwargs):
        """
        
        :param options: 
        :param kwargs: 
        :return: 
        """

        options = self.config_log_name(options, **kwargs)
        return options

    # noinspection PyUnusedLocal
    def config_log_name(self, options, **kwargs):
        """
        
        :param options: 
        :param kwargs: 
        :return: 
        """
        type(self).log_settings_configure(
            log_dir=options.log_base,
        )

        return options

    def config_file_names(self,
                          service_name=None,
                          config_extensions=None,
                          config_paths=None,
                          global_config_base=None,
                          local_config_base=None,
                          **kwargs):
        """
        
        :param service_name: 
        :param config_extensions: 
        :param config_paths: 
        :param global_config_base: 
        :param local_config_base: 
        :param kwargs: 
        :return: 
        """

        if not service_name:
            service_name = self.get_service_name(**kwargs)

        if not config_extensions:
            config_extensions = self.get_config_extensions(**kwargs)

        if not global_config_base:
            global_config_base = self.get_global_config_base(**kwargs)

        if not local_config_base:
            local_config_base = self.get_local_config_base(**kwargs)

        if not config_paths:
            config_paths = self.get_config_paths(**kwargs)

        for path in config_paths:
            path = path.strip()
            if config_extensions:
                for ext in config_extensions:
                    yield path.format(
                        global_config_base=global_config_base,
                        local_config_base=local_config_base,
                        service_name=service_name,
                        extension=ext,
                    )
            else:
                yield path

    def get_description(self, **_):
        """
        
        :param _: 
        :return: 
        """
        return self.__doc__

    def get_epilog(self, **_):
        """
        
        :param _: 
        :return: 
        """
        return self.__doc__

    def get_service_name(self, **_):
        """
        
        :param _: 
        :return: 
        """

        if self.DEFAULT_SERVICE_NAME:
            return self.DEFAULT_SERVICE_NAME

        name = type(self).__name__
        name = name.replace('Service', '')
        name = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1-\2', name).lower()

        return name

    def get_config_extensions(self, **_):
        """
        
        :param _: 
        :return: 
        """
        return self.DEFAULT_CONFIG_EXTENSIONS

    def get_global_config_base(self, **_):
        """
        
        :param _: 
        :return: 
        """
        return self.DEFAULT_GLOBAL_CONFIG_DIR

    def get_local_config_base(self, **_):
        """
        
        :param _: 
        :return: 
        """
        return self.DEFAULT_LOCAL_CONFIG_DIR

    def get_config_paths(self, **_):
        """
        
        :param _: 
        :return: 
        """
        return self.DEFAULT_CONFIG_PATHS

    def get_log_base(self, **kwargs):
        """
        
        :param kwargs: 
        :return: 
        """
        base_pattern = self.get_log_base_pattern(**kwargs)
        log_base = base_pattern.format(
            service_name=self.get_service_name(**kwargs)
        )
        return log_base

    def get_log_base_pattern(self, **_):
        """
        
        :param _: 
        :return: 
        """
        return self.DEFAULT_LOG_DIR_PATTERN

    def get_version(self, **_):
        """
        
        :param _: 
        :return: 
        """
        version = (
            "{version} for python {python}".format(
                version=self.DEFAULT_VERSION,
                python=platform.python_version()
            )
        )
        return version

    def run(self, *args, **kwargs):
        """
        
        :param args: 
        :param kwargs: 
        :return: 
        """
        raise NotImplementedError('no run')
