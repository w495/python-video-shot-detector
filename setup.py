#! /usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import platform
import os
import six
from distutils.core import setup
from subprocess import Popen, PIPE
from pip.req import parse_requirements

INSTALL_NAME = 'shot-detector'


AVAILABLE_VERSIONS = {
    '2.7':  "py27",
    '3.4':  "py34"
}


def get_modules():
    package_name = INSTALL_NAME.replace('-', '_')
    for root, _, _ in os.walk(package_name):
        if '__pycache__' not in root:
            module = root.replace('/', '.')
            yield module


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
    git_commit = six.text_type(git_commit, 'utf8')

    version = "{commit}-py-{python_version}".format(
        commit =git_commit,
        python_version=get_python_version()
    )
    return version


def get_long_description():
    return open('README.md').read()

setup(
        name=INSTALL_NAME,
        description='Python shot detector based on PyAV',
        version=get_package_version(),
        author='Ilya w495 Nikitin',
        author_email='w@w-495.ru',
        include_package_data=True,
        packages=list(
            get_modules()
        ),
        install_requires=list(
            get_requires()
        ),
        license='LICENSE.txt',
        entry_points={
            'console_scripts': [
                'shot-detector = shot_detector.tool:main',
            ],
        },
        long_description=get_long_description(),
)
