# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import math

import numpy as np
from scipy.fftpack import dct


from scipy.signal import detrend

from .stat_swfilter import StatSWFilter



from .min_std_regression_swfilter import MinStdRegressionSWFilter

import itertools


class NikitinSWFilter(MinStdRegressionSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):

        for window in window_seq:
            x_window = self.split(window, depth=depth, **kwargs)


            for index, item in enumerate(x_window):
                yield item

                # if index == 0:
                #     yield -0.1
                # else:
                #     yield item

    def replace_items(self, sequence, replacer=None, **kwargs):

        #
        # values = list(self.extract_values(sequence))
        # mean = self.get_mean(values, **kwargs)
        # std = self.get_std(values, **kwargs)
        #
        #
        # upper_values = list(
        #     item for item in values if item >= mean
        # )
        # lower_values = list(
        #     item for item in values if item < mean
        # )
        #
        #
        # direction = None
        # if lower_values and upper_values:
        #     upper_mean = self.get_mean(upper_values)
        #     lower_mean = self.get_mean(lower_values)
        #


        for index, item in enumerate(sequence):
            if not item.state:
                yield self.Atom(
                    index=item.index,
                    value=replacer,
                    state=True
                )
            else:
                yield item


    def update_objects(self,
                       objects,
                       features,
                       centre_samples=True,
                       **kwargs):
        """

        :param objects:
        :param features:
        :param _:
        :return:
        """

        # objects = itertools.islice(
        #     objects,
        #     0,
        #     None,
        #     32,
        # )

        for index, (obj, feature) in enumerate(
            itertools.izip(objects, features)
        ):
            yield self.update_object(
                obj=obj,
                feature=feature
            )
