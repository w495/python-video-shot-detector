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

    def apply_operator(self, other, op):
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
                        operator=op
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
        return self.apply_operator(other, operator.add)

    def __sub__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.sub)

    def __mul__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.mul)

    def __truediv__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.truediv)

    def __div__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.div)

    def __pow__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.pow)

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


    def __eq__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.eq)

    def __ne__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.ne)

    def __le__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.le)

    def __ge__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.ge)

    def __lt__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.lt)

    def __gt__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.gt)
