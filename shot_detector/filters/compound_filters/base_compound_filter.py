# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.filters import (
    Filter,
    DelayFilter,
)
from shot_detector.utils.log_meta import should_be_overloaded


class BaseCompoundFilter(Filter):
    """
        I'm not sure I need it.
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        super(Filter, self).__init__(**kwargs)
        self.delay = DelayFilter()

    @should_be_overloaded
    def result_filter(self, **kwargs):
        return self.delay

    def filter_objects(self, objects, **kwargs):
        result_filter = self.result_filter(**kwargs)
        return result_filter.filter_objects(objects, **kwargs)
