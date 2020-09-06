#!/usr/bin/env python

# [2020] - Se-Ran Jun - All Rights Reserved

from distutils.core import setup

setup(name='panfp',
      description='A package to predict pangenome-based metagenome prediction',
      long_description=readme,
      url='https://github.com/srjun/panfp',
      author='Se-Ran Jun',
      author_email= 'seran.jun@gmail.com',
      install_requests=requirements,
      version= '1.1.2',
      packages=['panfp'],
      scripts=['bin/panfp'])
