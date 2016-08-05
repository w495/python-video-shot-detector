# -*- coding: utf8 -*-

from __future__ import absolute_import

import logging
import logging.config
import os
import os.path

# import datetime
# STARTTIME = datetime.datetime.now()
# LOGTIME = STARTTIME.strftime("%Y-%m-%d-%H-%M-%S")
LOGTIME = 'last'

LOGDIR = "priv/logs"

if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)

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
            'filename': '%s/critical.%s.log' % (LOGDIR, LOGTIME),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 16,
            'delay': True,
            'formatter': 'default_formatter',
        },

        'error_logfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/error.%s.log' % (LOGDIR, LOGTIME),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 16,
            'delay': True,
            'formatter': 'default_formatter',

        },

        'warning_logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/warning.%s.log' % (LOGDIR, LOGTIME),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 16,
            'delay': True,
            'formatter': 'default_formatter',

        },

        'info_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/info.%s.log' % (LOGDIR, LOGTIME),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 16,
            'delay': True,
            'formatter': 'default_formatter',

        },

        'debug_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/debug.%s.log' % (LOGDIR, LOGTIME),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 16,
            'delay': True,
            'formatter': 'default_formatter',

        },

        'log_meta_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/log_meta.%s.log' % (LOGDIR, LOGTIME),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 16,
            'delay': True,
            'formatter': 'log_meta_formatter',
        },

        'video_info_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/video_info.%s.log' % (LOGDIR, LOGTIME),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 16,
            'delay': True,
            'formatter': 'default_formatter',
        },

        'py_warning_logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/py.warning.%s.log' % (LOGDIR, LOGTIME),
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


def start_logging():
    """

    """
    logging.config.dictConfig(CONFIG_DICT)



start_logging()
