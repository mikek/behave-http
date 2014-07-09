Feature: REST
  As an imaginary RESTful API client
  I want to make sure REST steps really work

  Background: Set target server address and headers
    Given I am using server "$TEST_SERVER"
    And I set base URL to "$TEST_URL"
    And I set Accept header to "application/json"
    And I set Content-Type header to "application/json"

  Scenario: Test HEAD request
    When I send a HEAD request to "head"
    Then the response status should be "200"

  Scenario: Test GET request
    When I send a GET request to "get"
    Then the response status should be "200"

  Scenario: Test POST request by checking we get the same JSON payload back
    When I send a POST request to "post"
    """
    {"title": "Some title", "number": 42}
    """
    Then the response status should be "201"
    And the JSON should be
    """
    {"title": "Some title", "number": 42}
    """

  Scenario: Test OPTIONS request
    When I send an OPTIONS request to "options"
    Then the response status should be "200"
    And the Allow header should be "HEAD, GET, OPTIONS"

  Scenario: Test PUT request by checking we get the same revision back
    When I send a PUT request to "put"
    """
    {"rev": 2, "id": "foo"}
    """
    Then the response status should be "200"
    And the JSON at path "rev" should be 2

  Scenario: Test PATCH request
    When I send a PATCH request to "patch"
    """
    {"rev": 1}
    """
    Then the response status should be "200"
    And the JSON at path "rev" should be 1

  Scenario: Test DELETE request
    When I send a DELETE request to "delete"
    Then the response status should be "204"

  Scenario: Test TRACE request
    Given I set X-Foo header to "bar"
    When I send a TRACE request to "trace"
    Then the response status should be "200"
    And the response body should contain "X-Foo: bar"

  Scenario: Test GET request to URL with query string
    When I send a GET request to "get/args?foo=Some foo&bar=chocolate"
    Then the response status should be "200"
    And the JSON should be
    """
    {"foo": "Some foo", "bar": "chocolate"}
    """
