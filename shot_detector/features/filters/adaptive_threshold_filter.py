# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

import numpy as np

from .base_sliding_window_filter import BaseSlidingWindowFilter

class AdaptiveThresholdFilter(BaseSlidingWindowFilter):
    
    __logger = logging.getLogger(__name__)
    
    def aggregate_window(self, features, window_state, sigma_num = 3, *args, **kwargs):
        if(not window_state.is_empty):
            feature_values = window_state.values()
        else:
            feature_values = [features]
        value_mean = self.get_mean(feature_values)
        value_std = self.get_std(feature_values, value_mean)
        thresold_max = self.get_thresold(value_mean, value_std, sigma_num)
        return thresold_max, window_state

    def get_mean(self, feature_values):
        feature_values_len = len(feature_values)
        value_mean = sum(feature_values) / feature_values_len
        return value_mean
    
    def get_std(self, feature_values, value_mean):
        feature_values_len = len(feature_values)
        std_list = []
        for feature in feature_values:
            diff  = feature - value_mean
            std_list += [diff*diff]
        value_std = np.sqrt(sum(std_list)) / feature_values_len
        
        return value_std
    
    def get_thresold(self, value_mean, value_std, sigma_num = 3):
        thresold_max = value_mean + value_std * sigma_num
        return thresold_max

    def merge_features(self, 
                       original_features, 
                       aggregated_features, 
                       video_state, 
                       window_limit = -1, 
                       *args, **kwargs
                       ):
        window_state = self.get_window_state(video_state)
        diffefence = 0
        if (window_state.item_counter > window_limit):
            diffefence = (original_features - aggregated_features)
        return diffefence, video_state
