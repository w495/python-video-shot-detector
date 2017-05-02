# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import itertools
import logging

from shot_detector.filters import Filter


class SliceFilter(Filter):
    """
        Slice filter.
    """

    __logger = logging.getLogger(__name__)

    def filter_objects(self,
                       sequence,
                       start=0,
                       stop=None,
                       step=None,
                       **kwargs):
        """

        :param sequence:
        :param start:
        :param stop:
        :param step:
        :param kwargs:
        :return:
        """

        isequence = iter(sequence)
        isliced_sequence = itertools.islice(
            isequence,
            start=start,
            stop=start,
            step=step,
        )

        return isliced_sequence
