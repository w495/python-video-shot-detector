# -*- coding: utf8 -*-


from __future__ import absolute_import, division, print_function

class BaseNorm(object):

    def norm(self, vector, video_state, *args, **kwargs):
        res, video_state = self.__class__.length(vector, video_state, *args, **kwargs)
        return res, video_state



    @classmethod
    def length(cls, vector, video_state, *args, **kwargs):
        '''
            calculate_distance
            Should be implemented
        '''
        return vector, video_state


