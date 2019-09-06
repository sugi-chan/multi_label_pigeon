#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command
import setuptools

NAME='multi-label-pigeon-jupyter'
AUTHOR="Michael Sugimura"
EMAIL="michaelsugimura@gmail.com"
DESCRIPTION="A way to label multi label image datasets in jupyter"
URL="https://https://github.com/sugi-chan/multi_label_pigeon"

REQUIRED = [
    'ipywidgets'
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, 'multi_label_pigeon', '__version__.py')) as f:
    exec(f.read(), about)



setuptools.setup(
     name=NAME,  
     version=about['__version__'],
     #scripts=['multi_label_pigeon'] ,
     author=AUTHOR,
     author_email="deepak.kumar.iet@gmail.com",
     description=DESCRIPTION,
     long_description=long_description,
   long_description_content_type="text/markdown",
     url=URL,
     packages=setuptools.find_packages(),
     install_requires=REQUIRED,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
