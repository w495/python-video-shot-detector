# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter

from shot_detector.utils.dsl_kwargs import dsl_kwargs_decorator
import numpy as np

from sklearn.tree import DecisionTreeRegressor

class DecisionTreeRegressorSWFilter(BaseStatSWFilter):
    """
        Sliding window filter that uses DecisionTreeRegressor.


    """

    __logger = logging.getLogger(__name__)

    @dsl_kwargs_decorator(
        ('regressor_depth', int, 'd', 'rd', 'depth'),
    )
    def aggregate_windows(self,
                          window_seq,
                          regressor_depth=1,
                          **kwargs):
        """
        Reduce sliding windows into values

        :param collections.Iterable[SlidingWindow] window_seq:
            sequence of sliding windows
        :param int regressor_depth:
        :param kwargs: ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]
        """

        regressor = DecisionTreeRegressor(
            max_depth=regressor_depth
        )

        for window in window_seq:
            samples = (
                tuple( (i,) for i in xrange(len(window)))
            )
            regressor.fit(samples, window)
            predicted = regressor.predict(samples)
            for predicted_item in predicted:
                yield predicted_item

