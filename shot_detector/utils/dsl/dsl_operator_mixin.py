# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import operator

from past.utils import old_div


class DslOperatorMixin(object):
    """
        Basic feature filter
    """
    __logger = logging.getLogger(__name__)

    OPERATOR_LEFT = object()
    OPERATOR_RIGHT = object()

    def apply_operator(self,
                       op_func=None,
                       others=None,
                       op_mode=None,
                       **kwargs):
        raise NotImplementedError('no apply_operator')

    def __add__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.add,
            others=[other],
        )
        return op_result

    def __radd__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.add,
            others=[other],
            op_mode=self.OPERATOR_RIGHT,
        )
        return op_result

    def __sub__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.sub,
            others=[other],
        )
        return op_result

    def __rsub__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.sub,
            others=[other],
            op_mode=self.OPERATOR_RIGHT,
        )
        return op_result

    def __mul__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.mul,
            others=[other],
        )
        return op_result

    def __rmul__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.mul,
            others=[other],
            op_mode=self.OPERATOR_RIGHT,
        )
        return op_result

    def __truediv__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.truediv,
            others=[other],
        )
        return op_result

    def __rtruediv__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.truediv,
            others=[other],
            op_mode=self.OPERATOR_RIGHT,
        )
        return op_result

    def __div__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=old_div,
            others=[other],
        )
        return op_result

    def __rdiv__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=old_div,
            others=[other],
            op_mode=self.OPERATOR_RIGHT,
        )
        return op_result

    def __floordiv__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.floordiv,
            others=[other],
        )
        return op_result

    def __rfloordiv__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.floordiv,
            others=[other],
            op_mode=self.OPERATOR_RIGHT,
        )
        return op_result

    def __pow__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.pow,
            others=[other],
        )
        return op_result

    def __rpow__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.pow,
            others=[other],
            op_mode=self.OPERATOR_RIGHT,
        )
        return op_result

    def __eq__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.eq,
            others=[other],
        )
        return op_result

    def __ne__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.ne,
            others=[other],
        )
        return op_result

    def __le__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.le,
            others=[other],
        )
        return op_result

    def __ge__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.ge,
            others=[other],
        )
        return op_result

    def __lt__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.lt,
            others=[other],
        )
        return op_result

    def __gt__(self, other):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=operator.gt,
            others=[other],
        )
        return op_result

    @classmethod
    def tuple(cls, first, *args):
        """
        :param Filter first:
        :param Filter second:
        :return:
        """
        return first.append(*args)

    def append(self, *args):
        """
        :param other:
        :return:
        """
        op_result = self.apply_operator(
            op_func=DslOperatorMixin.tuple_op,
            others=args,
            op_mode=self.OPERATOR_LEFT,
        )
        return op_result

    @classmethod
    def tuple_op(cls, *args):
        """

        :return: 
        """
        return tuple(args)
