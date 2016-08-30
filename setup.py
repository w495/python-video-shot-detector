#! /usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function

from distutils.core import setup
from subprocess import Popen, PIPE

popen = Popen(
        ['git', 'describe', '--tags'],
        stdout=PIPE,
        stderr=PIPE)

git_commit, _ = popen.communicate()
git_commit = git_commit.strip()

setup(
        name='shot-detector',
        description='Python shot detector based on PyAV',
        version=git_commit,
        author='Ilya w495 Nikitin',
        author_email='w@w-495.ru',
        include_package_data=True,
        packages=[
            'shot_detector',
            'shot_detector.detectors',
            'shot_detector.features',
            'shot_detector.features.extractors',
            'shot_detector.features.extractors.colours',
            'shot_detector.features.extractors.features',
            'shot_detector.features.metrics',
            'shot_detector.features.norms',
            'shot_detector.filters',
            'shot_detector.filters.compound_filters',
            'shot_detector.filters.sliding_window_filters',
            'shot_detector.filters.sliding_window_filters.stat_test_swfilters',
            'shot_detector.handlers',
            'shot_detector.objects',
            'shot_detector.plotters',
            'shot_detector.plotters.event',
            'shot_detector.plotters.event.threshold',
            'shot_detector.plotters.event.threshold.static',
            'shot_detector.selectors',
            'shot_detector.selectors.event',
            'shot_detector.selectors.point',
            'shot_detector.services',
            'shot_detector.utils',
            'shot_detector.utils.collections',
            'shot_detector.utils.collections.sliding_windows',
            'shot_detector.utils.multiprocessing',
        ],
        license='LICENSE.txt',
        entry_points={
            'console_scripts': [
                'shot-detector = shot_detector:main',
            ],
        },
        long_description=open('README.md').read(),
)
