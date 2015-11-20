#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='combinatorix',
    version='0.1',
    author='Amirouche Boubekki',
    author_email='amirouche@hypermove.net',
    url='https://github.com/amirouche/combinatorix',
    description='Simple parser combinators',
    long_description=read('README.rst'),
    py_modules=['combinatorix'],
    zip_safe=False,
    license='LGPLv2.1 or later',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
