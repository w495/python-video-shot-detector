#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from shot_detector.utils import LogSetting
from .services import ShotDetectorPlotService


def main():
    """
    
    :return: 
    """
    log_setting = LogSetting(
        script_name='shot-detector-plot'
    )
    service = ShotDetectorPlotService(
        log_setting=log_setting
    )
    service.run()


if __name__ == '__main__':
    main()
