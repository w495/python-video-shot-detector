# -*- coding: utf-8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import sys

import tqdm


class TqdmHandler(logging.Handler):
    terminator = '\n'

    def __init__(self, stream=None):
        super(self.__class__, self).__init__()
        if stream is None:
            stream = sys.stderr
        self.stream = stream

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg, file=self.stream)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
