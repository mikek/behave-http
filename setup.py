from ez_setup import use_setuptools
import os
import sys

use_setuptools()
from setuptools import setup

# Installing pandoc just to convert Markdown to reStructuredText seems to be
# an overkill. And Markdown has more awesomeness.
long_description = open('README.md', 'r').read()

setup_requires = []

install_requires = [
    'behave>=1.2.4',
    'decorator>=3.4.0',
    'Jinja2==2.6',
    'jpath==1.2',
    'nose==1.2.1',
    'purl>=0.8',
    'requests>=2.3.0,<2.4',
]

tests_require = ['flask']

setup(
    name='behave-http',
    version='0.0.1',
    packages=['behave_http', 'behave_http.steps'],
    setup_requires=setup_requires,
    install_requires=install_requires,
    extras_require={
        'testing': tests_require,
    },
    description="Behave HTTP steps",
    long_description=long_description,
    url='https://github.com/mikek/behave-http',
    author='Mikhail Kolesnik',
    author_email='mike@openbunker.org',
    license='BSD 2-Clause',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Testing',
    ],
)
