#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import dirname, abspath, join, isfile
import platform

cwd = abspath(dirname(__file__))
module_path = join(cwd, 'redis_semaphore', '__init__.py')
python_version = platform.python_version()
install_requires = []
version_line = [line for line in open(module_path)
                if line.startswith('__version_info__')][0]
__version__ = '.'.join(eval(version_line.split('__version_info__ = ')[-1]))


def install_requirements():
    req_path = join(cwd, 'requirements.txt')
    if isfile(req_path):
        with open(req_path) as f:
            mods = filter(lambda m: len(m) > 0, f.read().split('\n'))
        install_requires.extend(mods)


def read_file(filename):
    path = join(cwd, filename)
    if isfile(path):
        return open(path).read()


install_requirements()


setup(
    name='Redis-Semaphore',
    version=__version__,
    description="A distributed semaphore and mutex built on Redis.",
    long_description=read_file('README.rst'),
    license='MIT',
    author='bluele',
    author_email='jksmphone@gmail.com',
    url='https://github.com/bluele/redis-semaphore',
    classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    packages=find_packages(),
    keywords='redis semaphore',
    install_requires=install_requires,
    zip_safe=False
)
