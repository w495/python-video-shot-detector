# -*- coding: utf8 -*-

from __future__ import absolute_import

import os
import os.path
import logging
import datetime
import logging.config


#STARTTIME = datetime.datetime.now()
#LOGTIME = STARTTIME.strftime("%Y-%m-%d-%H-%M-%S")
LOGTIME = ''



LOGDIR =  "priv/logs"

if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)

CONFIGDICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'default_formater': {
            'format':   '%(asctime)s %(levelname)s '
                        '<%(process)d %(threadName)s>\t%(name)s:\t'
                        '%(message)s '
        },
    },
    'handlers': {

        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default_formater',
        },

        'devel_critical_logfile':{
            'level' : 'CRITICAL',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/devel.critical.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter'     : 'default_formater',
        },

        'devel_error_logfile':{
            'level' : 'ERROR',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/devel.error.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter': 'default_formater',

        },

        'devel_warning_logfile':{
            'level' : 'WARNING',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/devel.warning.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter': 'default_formater',

        },

        'devel_info_logfile':{
            'level' : 'INFO',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/devel.info.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter': 'default_formater',

        },

        'devel_degug_logfile':{
            'level' : 'DEBUG',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/devel.degug.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter': 'default_formater',

        },


        'devel_funcall_logfile':{
            'level' : 'DEBUG',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/devel.funcall.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter': 'default_formater',
        },

        'devel_request_logfile':{
            'level' : 'DEBUG',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/devel.request.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter': 'default_formater',
        },

        'devel_client_logfile':{
            'level' : 'DEBUG',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/devel.client.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter': 'default_formater',
        },

        'py_warning_logfile':{
            'level' : 'WARNING',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : '%s/py.warning.%s.log' % (LOGDIR, LOGTIME),
            'when'          : 'midnight',
            'interval'      :   1,
            'backupCount'   :   16,
            'delay'         :   True,
            'formatter': 'default_formater',

        },

    },
    'loggers': {
        'apps.funcall':{
            'handlers': [
                'devel_funcall_logfile'
            ],
            'level': "INFO",
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
                'devel_critical_logfile',
                'devel_error_logfile',
                'devel_warning_logfile',
                'devel_info_logfile',
                'devel_degug_logfile',
            ],
            'level': "DEBUG",
        },
    }
}

def start_logging():
    logging.config.dictConfig(CONFIGDICT)
