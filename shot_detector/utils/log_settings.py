# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import datetime
import logging
import logging.config
import os
import os.path
import sys


class LogSetting(object):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    DEFAULT_LOG_DIR_PATTERN = '/var/log/{script_name}'

    def __init__(self,
                 name=None,
                 filters=None,
                 formatters=None,
                 handlers=None,
                 loggers=None,
                 config_dict=None,
                 script_name=None,
                 log_dir=None,
                 log_dir_pattern=None,
                 **kwargs):

        self.name = __name__
        if name:
            self.name = name

        self._logger = logging.getLogger(self.name)
        self._start_time = datetime.datetime.now()
        self._shadow_log_time = self._start_time.strftime(
            "%Y-%m-%d-%H-%M-%S"
        )

        self._log_time = 'last'
        self._log_dir = self.ensure_log_dir(
            script_name=script_name,
            log_dir=log_dir,
            log_dir_pattern=log_dir_pattern,
            **kwargs
        )

        self._filters = filters
        if not self._filters:
            self._filters = self.default_filters

        self._formatters = formatters
        if not self._formatters:
            self._formatters = self.default_formatters

        self._handlers = handlers
        if not self._handlers:
            self._handlers = self.default_handlers

        self._loggers = loggers
        if not self._loggers:
            self._loggers = self.default_loggers

        self._config_dict = config_dict
        if not self._config_dict:
            self._config_dict = self.default_config_dict

    @property
    def logger(self):
        """
        
        :return: 
        """
        return self._logger

    @property
    def internal_logger(self):
        """
        
        :return: 
        """
        return self.__logger

    def ensure_log_dir(self,
                       log_dir=None,
                       log_dir_pattern=None,
                       script_name=None,
                       **_):
        """
        
        :param log_dir: 
        :param log_dir_pattern: 
        :param script_name: 
        :param _: 
        :return: 
        """
        if not log_dir_pattern:
            log_dir_pattern = self.DEFAULT_LOG_DIR_PATTERN
        if not script_name:
            script_name = os.path.basename(sys.argv[0])
        if not log_dir:
            log_dir = log_dir_pattern.format(
                script_name=script_name
            )
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    def configure(self, config_dict=None, **kwargs):
        """
        
        :param config_dict: 
        :param kwargs: 
        :return: 
        """
        if not config_dict:
            config_dict = dict(**kwargs)
        config_dict = dict(config_dict, **self.config_dict)
        result = self._configure(config_dict)
        return result

    @staticmethod
    def _configure(config_dict):
        """
        
        :param config_dict: 
        :return: 
        """
        logging.config.dictConfig(config_dict)
        return dict(
            config_dict=config_dict,
        )

    @property
    def config_dict(self):
        """
        
        :return: 
        """
        return self._config_dict

    @property
    def filters(self):
        """
        
        :return: 
        """
        return self._filters

    @property
    def formatters(self):
        """
        
        :return: 
        """
        return self._formatters

    @property
    def handlers(self):
        """
        
        :return: 
        """
        return self._handlers

    @property
    def loggers(self):
        """
        
        :return: 
        """
        return self._loggers

    @property
    def default_config_dict(self):
        """
        
        :return: 
        """
        config_dict = {'version': 1,
                       'disable_existing_loggers': False,
                       'filters': self.filters,
                       'formatters': self.formatters,
                       'handlers': self.handlers,
                       'loggers': self.loggers}
        return config_dict

    @property
    def default_filters(self):
        """
        
        :return: 
        """
        return dict()

    @property
    def default_formatters(self):
        """
        
        :return: 
        """
        # noinspection PyPep8
        formatters = {
            #
            # %(asctime)s           Human-readable time when the LogRecord
            #                       was created. By default this is of the form
            #                       `2003-07-08 16:49:45,896`. The numbers after
            #                       the comma are millisecond portion of the time.
            #
            # %(created)f           Time when the LogRecord was created as returned
            #                       by `time.time()`.
            #
            # %(filename)s          Filename portion of pathname.
            #
            # %(funcName)s          Name of function containing the logging call.
            #
            # %(levelname)s         Text logging level for the message ('DEBUG',
            #                       'INFO', 'WARNING', 'ERROR', 'CRITICAL').
            #
            # %(levelno)s           Numeric logging level for the message ('DEBUG',
            #                       'INFO', 'WARNING', 'ERROR', 'CRITICAL').
            #
            # %(lineno)d            Source line number where the logging call
            #                       was issued (if available).
            #
            # %(module)s            Module (name portion of filename).
            #
            # %(msecs)d             Millisecond portion of the time when
            #                       the LogRecord was created.
            #
            # %(message)s           The logged message, computed as msg % args.
            #                       This is set when Formatter.format() is invoked.
            #
            # %(name)s              Name of the logger used to log the call.
            #
            # %(pathname)s          Full pathname of the source file where
            #                       the logging call was issued (if available).
            #
            # %(process)d           Process ID (if available).
            #
            # %(processName)s       Process name (if available).
            #
            # %(relativeCreated)d   Time in milliseconds when the LogRecord
            #                       was created, relative to the time
            #                       the logging module was loaded.
            #
            # %(thread)d            Thread ID (if available).
            #
            # %(threadName)s        Thread name (if available).
            #

            'default_file_formatter': {
                'format': '%(asctime)s %(levelname)s '
                          '<%(process)d %(threadName)s> '
                          ' %(module)s '
                          '%(name)s:'
                          '/%(funcName)s: '
                          '%(message)s '
            },
            'log_meta_file_formatter': {
                'format': '%(asctime)s %(levelname)s '
                          '<%(process)d %(threadName)s> '
                          '%(message)s '
            },
            'preface_file_formatter': {
                'format': '%(asctime)s %(levelname)s '
                          '<%(process)d %(threadName)s> '
                          '%(message)s '
            },
            'default_console_formatter': {
                '()': 'colorlog.ColoredFormatter',
                'log_colors': {
                    'DEBUG': 'bold_cyan',
                    'INFO': 'bold_green',
                    'WARNING': 'bold_yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
                'format': '%(log_color)s%(asctime)s %(levelname)s '
                          '<%(process)d %(threadName)s> '
                          '%(module)s: '
                          '%(name)s: '
                          '%(message)s '
            },
            'log_meta_console_formatter': {
                '()': 'colorlog.ColoredFormatter',
                'log_colors': {
                    'DEBUG': 'purple'
                },
                'format': '%(log_color)s %(asctime)s %(levelname)s '
                          '<%(process)d %(threadName)s> '
                          '%(module)s: '
                          '%(message)s '
            },
            'preface_console_formatter': {
                '()': 'colorlog.ColoredFormatter',
                'log_colors': {
                    'INFO': 'purple',
                },
                'format': '%(log_color)s %(asctime)s %(levelname)s '
                          '%(module)s: '
                          '%(message)s '
            }
        }
        return formatters

    @property
    def default_handlers(self):
        """
        
        :return: 
        """
        handlers = {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default_console_formatter',
            },
            'log_meta_console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'log_meta_console_formatter',
            },
            'preface_console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'preface_console_formatter',
            },
            'critical_logfile': {
                'level': 'CRITICAL',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '{log_dir}/critical.{log_time}.log'.format(
                    log_dir=self.log_dir,
                    log_time=self.log_time),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_file_formatter',
            },
            'error_logfile': {
                'level': 'ERROR',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '{log_dir}/error.{log_time}.log'.format(
                    log_dir=self.log_dir,
                    log_time=self.log_time),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_file_formatter',

            },
            'warning_logfile': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '{log_dir}/warning.{log_time}.log'.format(
                    log_dir=self.log_dir,
                    log_time=self.log_time),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_file_formatter',

            },
            'info_logfile': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '{log_dir}/info.{log_time}.log'.format(
                    log_dir=self.log_dir,
                    log_time=self.log_time),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_file_formatter',

            },
            'debug_logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '{log_dir}/debug.{log_time}.log'.format(
                    log_dir=self.log_dir,
                    log_time=self.log_time),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_file_formatter',

            },
            'log_meta_logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '{log_dir}/log_meta.{log_time}.log'.format(
                    log_dir=self.log_dir,
                    log_time=self.log_time),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'log_meta_file_formatter',
            },
            'py_warning_logfile': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '{log_dir}/py.warn.{log_time}.log'.format(
                    log_dir=self.log_dir,
                    log_time=self.log_time
                ),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_file_formatter',

            },
        }
        return handlers

    @property
    def log_time(self):
        """
        
        :return: 
        """
        return 'last'

    @property
    def log_dir(self):
        """
        
        :return: 
        """
        return self._log_dir

    @property
    def start_time(self):
        """
        
        :return: 
        """
        return self._start_time

    @property
    def default_loggers(self):
        """
        
        :return: 
        """
        loggers = {
            'shot_detector.utils.log_meta': {
                'handlers': [
                    'log_meta_logfile'
                ],
                'level': "INFO",
            },

            'shot_detector.handlers.base_handler': {
                'handlers': [
                    'preface_console'
                ],
                'level': "INFO",
                'propagate': False
            },

            'shot_detector.utils'
            '.multiprocessing.base_queue_process_pool': {
                'handlers': [
                    'console'
                ],
                'level': "DEBUG",
            },

            'libav': {
                'handlers': [
                    'console'
                ],
                'level': "DEBUG",
            },

            'multiprocessing': {
                'handlers': [
                    'console'
                ],
                'level': "DEBUG",
            },

            'py.warns': {
                'handlers': [
                    'py_warning_logfile'
                ],
                'level': "DEBUG",
            },
            '': {
                'handlers': [
                    'console',
                    'critical_logfile',
                    'error_logfile',
                    'warning_logfile',
                    'info_logfile',
                    'debug_logfile',
                ],
                'level': "DEBUG",
            },
        }
        return loggers
