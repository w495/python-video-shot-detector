# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict

WINDOW_SIZE = 200

class BaseSlidingWindowState(object):

    features = {}
    point_counter  = 0
    window_counter = 0
    window_size    = WINDOW_SIZE
 
    def __init__(self, window_size = WINDOW_SIZE, *args, **kwargs):
        self.window_size = WINDOW_SIZE

    def update_features(self, features, window_size = WINDOW_SIZE):
        return self.store_features(
            features, 
            self.get_window_counter(
                window_size
            )
        )

    def get_window_counter(self, window_size = WINDOW_SIZE):
        self.window_size = window_size
        self.window_counter = self.point_counter
        if(self.window_size):
            self.window_counter %= self.window_size
        self.point_counter += 1
        return self.window_counter
    
    def store_features(self, features, window_counter):
        self.features[window_counter] = features
        return self.features
