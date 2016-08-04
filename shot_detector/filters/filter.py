# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
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
        from .filter_cast_features import FilterCastFeatures

        #
        # if (    isinstance(other, types.BuiltinFunctionType)
        #         or (
        #             type(other).__name__  == 'type'
        #             and other.__name__ in ('int', 'float')
        #         )
        # ):

        if not isinstance(other, Filter):
            other = FilterCastFeatures(
                cast=other,
            )
        return Filter(
            sequential_filters=[
                self, other
            ],
        )

    def apply_operator_left(self, other, op):
        return self.apply_operator(other, op, is_right=False)

    def apply_operator_right(self, other, op):
        return self.apply_operator(other, op, is_right=True)

    def apply_operator(self, other, op, is_right=False):
        """

        :param other:
        :param op:
        :return:
        """

        from .filter_operator import FilterOperator

        debug_dict = dict(
            action=dict(
                a_name=type(self).__name__,
                b_name=type(other).__name__,
                op_name=type(op).__name__,
            ),
            options=self._options
        )

        if not isinstance(other, Filter):
            other = self.scalar_to_filter(
                value=other,
            )

        return FilterOperator(
            parallel_filters=[self, other],
            operator=op,
            is_right=is_right,
            __debug_dict=debug_dict
        )

    def to_filter(self, value):
        if isinstance(value, collections.Iterable):
            return self.seq_to_filter(value)
        return self.scalar_to_filter(value)

    def seq_to_filter(self, value):
        from .filter_cast_seq_value import FilterCastSeqValue
        return FilterCastSeqValue(seq=value)

    def scalar_to_filter(self, value):
        from .filter_cast_scalar_value import FilterCastScalarValue
        return FilterCastScalarValue(value=value)

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
        return self.apply_operator_left(
            other,
            operator.add
        )

    def __radd__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_right(
            other,
            operator.add
        )

    def __sub__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_left(other, operator.sub)

    def __rsub__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_right(other, operator.sub)

    def __mul__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_left(other, operator.mul)

    def __rmul__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_right(other, operator.mul)

    def __truediv__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_left(other, operator.truediv)

    def __rtruediv__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_right(other, operator.truediv)

    def __div__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_left(other, operator.div)

    def __rdiv__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator_right(other, operator.div)

    def __pow__(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(other, operator.pow)

    def __rpow__(self, other):
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
        return self.sequential(other)

    def __ror__(self, other):
        """
        :param Filter other:
        :return:
        """

        return self.sequential(other)

    def join(self, other):
        """
        :param Filter other:
        :return:
        """
        return self.apply_operator(
            other,
            Filter.tuple_op
        )

    @classmethod
    def tuple(cls, first, second):
        """
        :param Filter other:
        :return:
        """
        return first.join(second)

    @classmethod
    def tuple_op(cls, a, b):
        return (a, b)

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
