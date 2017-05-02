# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .filter import Filter


class FilterCastScalarValue(Filter):
    """
        Casts input scalar `value` to filter-type.

        The main active method is `filter_feature_item`.
        To apply it you should pass parameter `value`
        to its' constructor.
    """

    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, value=None, **kwargs):
        return feature * 0 + value
