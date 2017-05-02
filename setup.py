#! /usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import

import platform
import sys
from subprocess import Popen, PIPE

from setuptools import setup, find_packages
from pip.req import parse_requirements


INSTALL_NAME = 'shot_detector'

INSTALL_SEGMENT = 'dev'

AVAILABLE_VERSIONS = {
    '2.7': "py27",
    '3.4': "py34"
}


def get_python_version():
    raw_python_version = platform.python_version()
    python_version = '.'.join(raw_python_version.split('.')[:-1])
    return python_version


def get_requires():
    python_version = get_python_version()
    if python_version not in AVAILABLE_VERSIONS:
        raise NotImplementedError(
                'there is no {name} for your python. '
                'Only for {available} is available.'.format(
                        name=INSTALL_NAME,
                        available=AVAILABLE_VERSIONS.keys()
                )
        )
    dir_name = AVAILABLE_VERSIONS.get(python_version)
    install_requirements = parse_requirements(
            "requirements/{dir_name}/requirements-pip.txt".format(
                    dir_name=dir_name
            ),
            session=False
    )
    requires = (str(ir.req) for ir in install_requirements)
    return requires


def get_package_version():
    popen = Popen(
            ['git', 'describe', '--tags'],
            stdout=PIPE,
            stderr=PIPE
    )

    git_commit, _ = popen.communicate()
    git_commit = git_commit.strip()


    PY3 = sys.version_info[0] == 3
    if PY3:
        text_type = str
    else:
        text_type = unicode


    git_commit = text_type(git_commit, 'utf8')

    vpart = git_commit.split('-')[:-1]

    if not vpart:
        vpart = '{commit}{segment}'.format(
            commit=git_commit,
            segment=INSTALL_SEGMENT
        )

    version = (INSTALL_SEGMENT.join(vpart))

    return version


def get_long_description():
    return open('README.rst').read()


setup(
        name=INSTALL_NAME,
        description='Python shot detector based on PyAV',
        version=get_package_version(),
        author='Ilya w495 Nikitin',
        author_email='w@w-495.ru',
        include_package_data=True,
        packages=find_packages(
            exclude=[
                'build*',
                'etc*',
                'priv*',
                'config*',
                'test*',
                'dist*',
            ]
        ),
        install_requires=list(
            get_requires()
        ),
        zip_safe=False,
        license='BSD',
        entry_points={
            'console_scripts': [
                'shot-detector = shot_detector.tool:main',
            ],
        },
        package_data={},
        long_description=get_long_description(),
        keywords="video-processing image-processing video",
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Telecommunications Industry",
            "License :: OSI Approved :: BSD License",
            "Natural Language :: English",
            "Natural Language :: Russian",
            "Topic :: Multimedia :: Graphics :: Capture",
            "Topic :: Multimedia :: Video :: Capture",
            "Topic :: Multimedia :: Video :: Non-Linear Editor",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Scientific/Engineering :: Mathematics",
            "Topic :: Utilities",
        ],
)
