# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from shot_detector.features.filters import (
    DelayFilter,
    SavitzkyGolaySWFilter
)

delay = DelayFilter()

polynomial_approximation = SavitzkyGolaySWFilter(
    window_size=25,
    strict_windows=True,
    polyorder=2,
    overlap_size=0,
)


def mole_filter(size=25):
    res = filter_generator(size)
    res = sum(res)/size
    return res


def filter_generator(size=25):
    for offset in xrange(size):
        yield delay(offset) | polynomial_approximation(s=25)
