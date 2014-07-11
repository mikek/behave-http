# Behave HTTP steps

*A Python package for HTTP-service testing. Contains reusable steps for
[behave][1] BDD (behaviour-driven development) tool.*

It's mostly useful for testing REST APIs and interacting with JSON data.

## Usage

*yourapp/features/environment.py*:

    from behave_http.environment import before_scenario

*yourapp/features/steps/some_http_stuff.py*:

    from behave_http.steps import *

(You can mix them with your own steps in the same file.)

*yourapp/features/some_api.feature*:

    Feature: Some API
      As an API client
      I want to be able to manage activities and sessions

      Background: Set server name, headers and reset test user's database
        Given I am using server "$SERVER"
        And I set base URL to "$URL"
        And I set Accept header to "application/json"
        And I set Content-Type header to "application/json"
        And I set BasicAuth username to "ft@example.com" and password to "ft"

      Scenario: Ensure account exists
        When I make a GET request to "account"
        Then the response status should be 200

If your test target is *http://127.0.0.1:8081/api* you can test it with:

    SERVER=http://127.0.0.1:8081 URL=api behave

General rules on using quoted `"values"` in feature files:

 * JSONs and numbers (response code, array length) must appear as is.
 * Other substitutes must be quoted (variable names, headers and their values).

See *features* (self tests) directory for some useful examples.

## Development

### Running tests

Launch a special HTTP server responding to test requests in a separate shell:

    python testserver.py

Then use `make` to run feature tests:

    make behave-test

or just:

    behave

#### Environment variables

Set *TEST_SERVER* to full URL (including schema) if default port (55080) on
localhost is already used by another process. For example:

    export TEST_SERVER=http://127.0.0.1:55081
    python testserver.py &
    make behave-test

## Acknowledgments

The REST steps code is initially derived from [rest api blueprint][2], so this
project inherits the same BSD 2-Clause License (see LICENSE file).

[1]: http://pythonhosted.org/behave/
[2]: https://bitbucket.org/tcorbettclark/rest-api-blueprint
