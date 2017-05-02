# -*- coding: utf8 -*-

from __future__ import absolute_import

import logging
import logging.config
import os
import sys
import os.path

# import datetime
# STARTTIME = datetime.datetime.now()
# LOG_TIME = STARTTIME.strftime("%Y-%m-%d-%H-%M-%S")


DEFAULT_LOG_DIR_PATTERN = '/var/log/{self_name}'

def ensure_log_dir(log_dir=None, pattern=None, self_name=None):

    if not pattern:
        pattern = DEFAULT_LOG_DIR_PATTERN

    if not self_name:
        self_name = os.path.basename(sys.argv[0])

    if not log_dir:
        log_dir = pattern.format(
            self_name=self_name
        )
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    return log_dir


def configure(*args, **kwargs):

    LOG_TIME = 'last'

    LOG_DIR = ensure_log_dir(*args, **kwargs)

    CONFIG_DICT = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {

        },
        'formatters': {

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

            'default_formatter': {
                'format': '%(asctime)s %(levelname)s '
                # '<%(process)d %(threadName)s> '
                          '%(name)s:'
                          '/%(funcName)s: '
                          '%(message)s '
            },
            'log_meta_formatter': {
                'format': '%(asctime)s %(levelname)s '
                # '<%(process)d %(threadName)s> '
                          '%(message)s '
            },
            'console_formatter': {
                '()': 'colorlog.ColoredFormatter',
                'log_colors': {
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
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
            },
        },
        'handlers': {

            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'console_formatter',
            },

            'preface_console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'preface_console_formatter',
            },

            'critical_logfile': {
                'level': 'CRITICAL',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/critical.%s.log' % (LOG_DIR, LOG_TIME),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_formatter',
            },

            'error_logfile': {
                'level': 'ERROR',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/error.%s.log' % (LOG_DIR, LOG_TIME),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_formatter',

            },

            'warning_logfile': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/warning.%s.log' % (LOG_DIR, LOG_TIME),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_formatter',

            },

            'info_logfile': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/info.%s.log' % (LOG_DIR, LOG_TIME),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_formatter',

            },

            'debug_logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/debug.%s.log' % (LOG_DIR, LOG_TIME),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_formatter',

            },

            'log_meta_logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/log_meta.%s.log' % (LOG_DIR, LOG_TIME),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'log_meta_formatter',
            },

            'video_info_logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/video_info.%s.log' % (LOG_DIR, LOG_TIME),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_formatter',
            },

            'py_warning_logfile': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/py.warning.%s.log' % (LOG_DIR, LOG_TIME),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 16,
                'delay': True,
                'formatter': 'default_formatter',

            },

        },
        'loggers': {

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

            'shot_detector.utils.multiprocessing.base_queue_process_pool': {
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

            'py.warnings': {
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
    }


    logging.config.dictConfig(CONFIG_DICT)

    return dict(
        config_dict=CONFIG_DICT,
        log_dir=LOG_DIR
    )

