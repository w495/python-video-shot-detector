# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging


from .base_nested_filter import BaseNestedFilter

class Filter(BaseNestedFilter):

    __logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super(Filter, self).__init__(*args, **kwargs)
        for attr, value in six.iteritems(kwargs):
            setattr(self, attr, value)


