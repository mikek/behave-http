# Behave HTTP steps

*A python package with reusable HTTP-service testing steps for [behave][1]
(behaviour-driven development tool).*

## Usage

*yourapp/features/environment.py*:

    from behave_http.environment import before_scenario

*yourapp/features/steps/some_http_stuff.py*:

    from behave_http.steps import rest

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
        When I send a GET request to "account"
        Then the response status should be "200

If your test target is *http://127.0.0.1:8081/api* you can test it with:

    SERVER=http://127.0.0.1:8081 URL=api behave

See *features* (self testing) directory for some useful examples.

## Acknowledgments

The REST steps code is derived from [rest api blueprint][2], so the whole
project use the same BSD 2-Clause License (see LICENSE file).

[1]: http://pythonhosted.org/behave/
[2]: https://bitbucket.org/tcorbettclark/rest-api-blueprint
