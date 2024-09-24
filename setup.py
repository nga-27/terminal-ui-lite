#!/usr/bin/env python
# Based on: https://github.com/kennethreitz/setup.py/blob/master/setup.py
"""
Setup tools
Use setuptools to install package dependencies. Instead of a requirements file you
can install directly from this file.
`pip install .`
You can install dev dependencies by targetting the appropriate key in extras_require
```
pip install .[dev] # install requires and test requires
pip install '.[dev]' # install for MAC OS / zsh

```
See: https://packaging.python.org/tutorials/installing-packages/#installing-setuptools-extras
"""
import re
import platform
import subprocess
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'terminal-ui-lite'
DESCRIPTION = 'A light-weight way to have a terminal as a basic UI for servers and non-graphical UIs'
URL = 'https://github.mmm.com/nga-27/terminal-ui-lite'
EMAIL = 'namell91@gmail.com'
AUTHOR = 'Nick Amell'
REQUIRES_PYTHON = '>=3.9.0, <3.13.0'
VERSION = '0.1.0'

# What packages are required for this module to be executed?
REQUIRES = [
    'colorama',
    'enhanced_input@git+ssh://git@github.com/nga-27/enhanced-input.git@v0.1.1'
]

REQUIRES_DEV = [
    'pylint==3.2.5',
    'pycodestyle==2.12.0',
]

def has_ssh() -> bool:
    result = None
    try:
        if 'windows' in platform.platform().lower():
            ssh_test = subprocess.run(['where', 'ssh'])
        else:
            ssh_test = subprocess.run(['which', 'ssh'])
    except Exception:
        print("EXCEPTION: ssh not found. Attempting https...")
        return False
    
    if ssh_test.returncode == 0:
        result = subprocess.Popen(
            ['ssh', '-Tq', 'git@github.com', '&>', '/dev/null']
        )
        result.communicate()
    if not result or result.returncode == 255:
        return False
    return True


def flip_ssh(requires: list) -> list:
    if not has_ssh():
        requires = list(map(lambda x: re.sub(r'ssh://git@', 'https://', x), requires))
    return requires


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=[
            "*.tests",
            "*.tests.*"
            "tests.*",
            "tests"
        ]
    ),
    install_requires=flip_ssh(REQUIRES),
    extras_require={
        'dev': flip_ssh(REQUIRES_DEV),
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
