# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(name="numerical_x", ext_modules=cythonize('numerical_x.pyx'),)