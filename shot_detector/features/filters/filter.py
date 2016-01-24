# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import operator

import six

from .base_nested_filter import BaseNestedFilter


class Filter(BaseNestedFilter):
    """
        Basic feature filter
    """
    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        super(Filter, self).__init__(**kwargs)
        for attr, value in six.iteritems(kwargs):
            setattr(self, attr, value)

    def sequential(self, other):
        """

        :param other:
        :return:
        """
        return Filter(
            sequential_filters=[
                self, other
            ]
        )

    def operator(self, other, op):
        """

        :param other:
        :param op:
        :return:
        """
        from .filter_operator import FilterOperator

        if isinstance(other, Filter):
            return FilterOperator(
                parallel_filters=[self, other],
                operator=op
            )
        else:
            return Filter(
                sequential_filters=[
                    self,
                    FilterOperator(
                        other=other,
                        operator=operator
                    )
                ]
            )

    def i(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return self.intersect(*args, **kwargs)

    def intersect(self, other, threshold=0):
        """

        :param other:
        :param threshold:
        :return:
        """
        from .filter_intersection import FilterIntersection

        return FilterIntersection(
            parallel_filters=[self, other],
            threshold=threshold
        )

    def __add__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.operator(other, operator.add)

    def __sub__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.operator(other, operator.sub)

    def __mul__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.operator(other, operator.mul)

    def __truediv__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.operator(other, operator.truediv)

    def __div__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.operator(other, operator.div)

    def __pow__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.operator(other, operator.pow)

    def __contains__(self, item):
        """
        :param Filter item:
        :return:
        """
        return self.intersect(item)

    def __or__(self, other):
        """
        :param Filter other:
        :return:
        """

        if isinstance(other, Filter):
            return self.sequential(other)
