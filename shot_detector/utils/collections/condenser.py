# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function


class Condenser(object):
    """
    Save pushed values into internal list
    If number of values equal to maximum size
    it return all values and make list empty.
    """

    MAXLEN = 1024

    def __init__(self, maxlen=MAXLEN):
        self._is_charged = False
        self.maxlen = maxlen
        self.list = []

    def charge(self, value):
        """
        Save pushed values into internal variable.
        If number of values equal to maximum size
        It flushes internal variable to empty.
        In this way «condenser» become «charged»

        :param value:
            any value
        :return: bool
            charged ot not (discharged)
        """
        if self._is_charged:
            self.list = []
        self._is_charged = False
        self.list += [value]
        if len(self.list) == self.maxlen:
            self._is_charged = True
        return self._is_charged

    @property
    def is_charged(self):
        return self._is_charged

    def get(self):
        """
        Returns:
            [If it is fully charged]
                list of all values from internal variable
                from the last discharge.
            [If it is not fully charged]
                empty list.

        :return: list
        """
        if self.is_charged:
            return self.list
        return []
