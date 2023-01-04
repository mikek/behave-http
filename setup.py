#!/usr/bin/env python

from distutils.core import setup

import os


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme_file:
    long_description = readme_file.read()

setup_requires = ["wheel"]

install_requires = [
    "behave>=1.2.4",
    "Jinja2>=2.5",
    "jpath>=1.1",
    "ensure>=0.1.6",
    "requests>=2.0.0",
    "six",
]

setup(
    setup_requires=setup_requires,
    install_requires=install_requires,
    description="Behave HTTP steps",
    long_description=long_description,
    url="https://github.com/mikek/behave-http",
    author="Mykhailo Kolesnyk",
    author_email="mike@openbunker.org",
    license="BSD 2-Clause",
    py_modules="behave_http",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Testing",
    ],
)
