# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from ..scipy_stat_swfilter import SciPyStatSWFilter


class BaseStatTestSWFilter(SciPyStatSWFilter):

    __logger = logging.getLogger(__name__)

    pass