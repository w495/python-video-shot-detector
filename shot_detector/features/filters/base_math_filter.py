# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

import numpy as np
from shot_detector.utils.numerical import gaussian_1d

from .base_filter import BaseFilter

class BaseMathFilter(BaseFilter):
    
    __logger = logging.getLogger(__name__)

    EPSILON = np.finfo(float).eps

    def bool(self, expresion, *args, **kwargs):        
        use_any = kwargs.pop('use_any', False)
        out_expresion = np.array(expresion)
        if(use_any):
            return out_expresion.any()
        return out_expresion.all()

    def gaussian_features(self, features, gaussian_sigma = None, *args, **kwargs):
        """
            gaussian_features = gaussian_1d (features)
        """
        size = len(features)
        gaussian_features = []
        for i, feature in enumerate(features):
            feature = gaussian_1d(
                x = feature, 
                size = size, 
                offset = 0, 
                sigma = gaussian_sigma
            )
            gaussian_features += [feature]
        return gaussian_features
    
    def sqrt(self, expresion, *args, **kwargs):        
        return np.sqrt(expresion)


    def escape_null(self, expresion):
        return expresion + self.EPSILON
    

    def log(self, expresion, *args, **kwargs):
        expr =  self.escape_null(expresion)
        return np.log(expr)
    
    def log10(self, expresion, *args, **kwargs):
        expr =  self.escape_null(expresion)
        return np.log10(expr)
    
    
    
    