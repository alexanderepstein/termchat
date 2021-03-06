#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'termchat'
DESCRIPTION = 'Chat through the terminal with hack.chat'
URL = 'https://github.com/alexanderepstein/termchat'
EMAIL = 'epsteina@wit.edu'
AUTHOR = 'Alexander Epstein'
VERSION = '0.0.4'
here = os.path.abspath(os.path.dirname(__file__))
long_description = "For information on this package refer to the github: " + URL
# What packages are required for this module to be executed?
required = [
     'websocket-client'
]

# Dependencies only for versions less than Python 2.7:
# if sys.version_info < (2, 7):
#     required.append('requests[security]')

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['termchat=termchatDriver.driver:main'],
    },
    keywords = ['terminal', 'chat', 'client', 'console'], # arbitrary keywords
    install_requires=required,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
