# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from sklearn.tree import DecisionTreeRegressor

from shot_detector.utils.dsl_kwargs import dsl_kwargs_decorator
from .base_stat_swfilter import BaseStatSWFilter


class DecisionTreeRegressorSWFilter(BaseStatSWFilter):
    # noinspection PyPep8
    """
    Sliding window filter that based on DecisionTreeRegressor.

    Let set the initial samples and data:

    >>> sample_list = list([i] for i in xrange(10))
    >>> sample_list
    [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
    >>> data_list = list(i for i in xrange(10))
    >>> data_list
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    The DecisionTreeRegressor builds crude approximation
    of initial data with initial samples. You can control
    the «crudeness» with `max_depth` parameter.
    See `regressor_depth` parameter of `aggregate_windows`.

    >>> regressor = DecisionTreeRegressor(max_depth=1)
    >>> _ = regressor.fit(sample_list, data_list)
    >>> regressor.predict(sample_list)
    array([ 2.,  2.,  2.,  2.,  2.,  7.,  7.,  7.,  7.,  7.])
    >>> regressor.predict([[4.5]])
    array([ 2.])
    >>> regressor.predict([[4.6]])
    array([ 7.])

    Let decrease the level of approximation to max_depth=2

    >>> regressor = DecisionTreeRegressor(max_depth=2)
    >>> _ = regressor.fit(sample_list, data_list)
    >>> regressor.predict(sample_list)
    array([ 0.5,  0.5,  3. ,  3. ,  3. ,  5.5,  5.5,  8. ,  8. ,  8. ])
    >>> regressor.predict([[4.5]])
    array([ 3.])
    >>> regressor.predict([[4.6]])
    array([ 5.5])

    Let decrease the level of approximation to max_depth=3.
    It is very close to initial data.

    >>> regressor = DecisionTreeRegressor(max_depth=3)
    >>> _ = regressor.fit(sample_list, data_list)
    >>> regressor.predict(sample_list)
    array([ 0. ,  1. ,  2. ,  3.5,  3.5,  5. ,  6. ,  7. ,  8.5,  8.5])
    >>> regressor.predict([[4.5]])
    array([ 3.5])
    >>> regressor.predict([[4.6]])
    array([ 5.])

    Let decrease the level of approximation to max_depth=4
    In this case we'll get the initial dataset.

    >>> regressor = DecisionTreeRegressor(max_depth=4)
    >>> _ = regressor.fit(sample_list, data_list)
    >>> regressor.predict(sample_list)
    array([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9.])
    >>> regressor.predict([[4]])
    array([ 4.])
    >>> regressor.predict([[4.5]])
    array([ 4.])
    >>> regressor.predict([[4.6]])
    array([ 5.])
    >>> regressor.predict([[1.5]])
    array([ 1.])
    >>> regressor.predict([[1.6]])
    array([ 2.])

    """

    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.

            Sets the minimal size for sliding window.
        """

        min_size = 1
        overlap_size = 0
        strict_windows = True
        cs = False

    @dsl_kwargs_decorator(
        ('normalize_predicted', bool, 'n', 'np', 'normalize'),
        ('regressor_depth', int, 'd', 'rd', 'depth'),
        ('mark_joint', int, 'm', 'j', 'mj'),
    )
    def aggregate_windows(self,
                          window_seq,
                          regressor_depth=1,
                          normalize_predicted=False,
                          mark_joint=None,
                          **kwargs):
        """
        Reduce sliding windows into values

        :param collections.Iterable[SlidingWindow] window_seq:
            sequence of sliding windows
        :param int regressor_depth:
            the depth of the regression tree in `DecisionTreeRegressor`,
        :param kwargs: ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]
        """

        regressor = DecisionTreeRegressor(
            max_depth=regressor_depth,
            # presort=True,
        )

        for w_index, window in enumerate(window_seq):
            samples = (
                tuple((i,) for i in xrange(len(window)))
            )
            regressor.fit(samples, window)
            predicted = regressor.predict(samples)

            if normalize_predicted:
                predicted = self._normalize(predicted)

            for p_index, predicted_item in enumerate(predicted):
                if p_index == 0 and mark_joint:
                    yield mark_joint
                else:
                    yield predicted_item

    @staticmethod
    def _normalize(vector):
        """

        :param vector:
        :return:
        """
        rng = vector.max() - vector.min()
        min_ = vector.min()
        return (vector - min_)
