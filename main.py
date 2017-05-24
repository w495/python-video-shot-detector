#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from shot_detector.tool import main

if __name__ == '__main__':
    main()



#
# import numpy as np
#
# from shot_detector.utils.numerical.numerical_x import shrink2d
#
# x = np.array([[1,2,3,4], [1,2,3,4], [1,2,3,4], [1,2,3,4]])
#
# x = np.array([[[1,2,3],[1,2,3],[1,2,3],[1,2,3]], [[1,2,3],[1,2,3],[1,2,3],[1,2,3]], [[1,2,3],[1,2,3],[1,2,3],[1,2,3]], [[1,2,3],[1,2,3],[1,2,3],[1,2,3]] ])
#
#
# print(shrink2d(x*1.0, 2, 2))