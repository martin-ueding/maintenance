#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>

from setuptools import setup, find_packages

setup(
    name = 'maintenance',
    version = "1.10.2",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'maintenance = maintenance:main',
        ],
    },
    scripts=[
        'my-clamscan',
    ],
    package_data={
        'maintenance': ['tasks/*'],
    },
)
