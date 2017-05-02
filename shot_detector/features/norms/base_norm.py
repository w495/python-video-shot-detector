# -*- coding: utf8 -*-


from __future__ import absolute_import, division, print_function


class BaseNorm(object):
    def norm(self, vector, **kwargs):
        length = self.__class__.length(vector, **kwargs)
        return length

    @classmethod
    def length(cls, vector, **kwargs):
        raise NotImplementedError('length')
