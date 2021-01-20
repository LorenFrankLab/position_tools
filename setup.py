#!/usr/bin/env python3

from setuptools import find_packages, setup

INSTALL_REQUIRES = ['numpy >= 1.11', 'scipy', 'opencv-python', 'tqdm']
TESTS_REQUIRE = ['pytest >= 2.7.1']

setup(
    name='position_tools',
    version='0.1.0.dev0',
    license='MIT',
    description=(''),
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
)
