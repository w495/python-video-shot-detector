#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function


from .services import ShotDetectorPlotService

def main():
    service = ShotDetectorPlotService()
    service.run()

if __name__ == '__main__':
    main()


