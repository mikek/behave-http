BDD HTTP steps implementation for Behave
========================================

|Build Status| |Coverage Status|

A Python package for HTTP-service testing. Contains reusable steps for
`Behave <http://pythonhosted.org/behave/>`_ BDD (behaviour-driven
development) tool. It’s mostly useful for testing REST APIs and interacting
with JSON data over HTTP.

Usage
-----

*yourapp/features/environment.py*:

::

    from behave_http.environment import before_scenario

*yourapp/features/steps/some\_http\_stuff.py*:

::

    from behave_http.steps import *

(You can mix them with your own steps in the same file.)

*yourapp/features/some\_api.feature*:

::

    Feature: Some API
      As an API client
      I want to be able to manage activities and sessions

      Background: Set server name, headers and reset test user's database
        Given I am using server "$SERVER"
        And I set base URL to "$URL"
        And I set "Accept" header to "application/json"
        And I set "Content-Type" header to "application/json"
        And I set BasicAuth username to "t@example.com" and password to "t"

      Scenario: Ensure account exists
        When I make a GET request to "account"
        Then the response status should be 200

If your test target is *http://127.0.0.1:8081/api* you can test it with:

::

    SERVER=http://127.0.0.1:8081 URL=api behave

General rules on using quoted ``"values"`` in feature files:

-  JSONs and numbers (response code, array length) must appear as is.
-  Other substitutes must be quoted (variable names, headers and their
   values).

While there is no extensive documentation the *features* (self tests)
directory contains (a hopefully complete) set of usage examples.

*Testing for nested JSON content with non-ASCII characters in paths is
not supported by the underlying ``jpath`` library.*

Development
-----------

To install essential packages for the test suite:

::

    pip install -r requirements_dev.txt

A complete list of development tools used in the ``Makefile`` can be installed
with:

::

    pip install coveralls docutils flake8 tox wheel

Running tests
~~~~~~~~~~~~~

Launch a special HTTP server responding to test requests:

::

    python testserver.py

Then run feature tests in a separate shell:

::

    make test-all # runs on every supported python version with tox
    make test     # runs in current python environment only

Environment variables
^^^^^^^^^^^^^^^^^^^^^

Set *TEST\_SERVER* to full URL (including schema) if default port
(55080) on localhost is already used by another process. For example:

::

    export TEST_SERVER=http://127.0.0.1:55081
    python testserver.py >testserver.log 2>&1 &
    make test-coverage

Acknowledgments
---------------

The REST steps code is initially derived from *rest api blueprint* [1]_,
so this project inherits the same BSD 2-Clause License (see LICENSE
file).

.. [1] https://bitbucket.org/tcorbettclark/rest-api-blueprint

.. |Build Status| image:: http://img.shields.io/travis/mikek/behave-http/master.svg
   :target: https://travis-ci.org/mikek/behave-http
.. |Coverage Status| image:: http://img.shields.io/coveralls/mikek/behave-http/master.svg
   :target: https://coveralls.io/r/mikek/behave-http?branch=master
