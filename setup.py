import os

from setuptools import setup
from setuptools.command.test import test as TestCommand

# Gotcha: setuptools_behave module is unavailable before 'setup.py install'
try:
    from setuptools_behave import behave_test as BehaveTest
    # Nested gotcha: setuptools_behave is unable to find 'behave' command.
    # TODO: make sure it has no side-effects and make a PR.
    import shlex
    import subprocess

    class CustomBehaveTest(BehaveTest):
        def behave(self, path):
            behave = os.path.join("bin", "behave")
            if not os.path.exists(behave):
                behave = "behave"
            cmd_options = ""
            if self.tags:
                cmd_options = "--tags=" + " --tags=".join(self.tags)
            if self.dry_run:
                cmd_options += " --dry-run"
            cmd_options += " --format=%s %s" % (self.format, path)
            self.announce("CMDLINE: %s %s" % (behave, cmd_options), level=3)
            return subprocess.call([behave] + shlex.split(cmd_options))
except ImportError:
    class CustomBehaveTest(TestCommand):
        description = "Dummy behave test command used before setup.py install"


# Installing pandoc just to convert Markdown to reStructuredText seems to be
# an overkill. And Markdown has more awesomeness.
long_description = open('README.md', 'r').read()

setup_requires = []

install_requires = [
    'behave>=1.2.4',
    'decorator>=3.4.0',
    'Jinja2==2.6',
    'jpath==1.2',
    'ensure>=0.2.1',
    'purl>=0.8',
    'requests>=2.3.0,<2.4',
]

# Flask is required for running test webserver
tests_require = ['flask']

setup(
    name='behave-http',
    version='0.0.1',
    packages=['behave_http', 'behave_http.steps'],
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'testing': tests_require,
    },
    cmdclass={
        'behave_test': CustomBehaveTest,
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
