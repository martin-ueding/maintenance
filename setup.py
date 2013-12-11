#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

from setuptools import setup, find_packages

setup(
    name = 'maintenance',
    version = "1.7.20",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'maintenance = maintenance:main',
        ],
    },
)
