#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
from setuptools import setup, find_packages

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def read_reqs(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return [line for line in f.read().split('\n') if line and not line.strip().startswith('#')]

tests_require = []  # mostly handled by tox
if sys.version_info < (2, 7):
    tests_require.append("unittest2 == 0.5.1")  # except this

def read_version():
    with open(os.path.join('lib', 'astunparse', '__init__.py')) as f:
        m = re.search(r'''__version__\s*=\s*['"]([^'"]*)['"]''', f.read())
        if m:
            return m.group(1)
        raise ValueError("couldn't find version")


setup(
    name='astunparse',
    version=read_version(),
    description='An AST unparser for Python',
    long_description=readme + '\n\n' + history,
    maintainer='Simon Percivall',
    maintainer_email='percivall@gmail.com',
    url='https://github.com/simonpercivall/astunparse',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    include_package_data=True,
    install_requires=read_reqs('requirements.txt'),
    license="BSD",
    zip_safe=False,
    keywords='astunparse',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Code Generators',
    ],
    test_suite='tests',
    tests_require=tests_require,
)
