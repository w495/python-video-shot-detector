# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from .base_sliding_window_filter import BaseSlidingWindowFilter


import numpy as np


class AdaptiveThresholdFilter(BaseSlidingWindowFilter):

    def aggregate_window(self, features, window_state, sigma_num = 3, *args, **kwargs):
        
        
        #print ('window_state.window_counter = ', window_state.window_counter)
        if(window_state.point_counter):
            feature_values = window_state.values()
        else:
            feature_values = [features]
        value_mean = self.get_mean(feature_values)
        value_std = self.get_std(feature_values, value_mean)
        thresold_max = self.get_thresold(value_mean, value_std, sigma_num)
        
        
        #print ('thresold_max = ', thresold_max)

        
        #print ('features = ', features)
        
        
        return value_mean, window_state

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

    def merge_features(self, original_features, aggregated_features, video_state, *args, **kwargs):
        diffefence = (original_features - aggregated_features)
        
        
        return diffefence, video_state
