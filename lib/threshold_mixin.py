# -*- coding: utf8 -*-

from __future__ import absolute_import



class ThresholdMixin(object):

    def handle_features(self, features, shot_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return shot_state
