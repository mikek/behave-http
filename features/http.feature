Feature: HTTP requests
  As an imaginary HTTP API client
  I want to make sure HTTP steps do what they meant to do

  Background: Set target server address and headers
    Given I am using server "$TEST_SERVER"
    And I set base URL to "$TEST_URL"
    And I set Accept header to "application/json"
    And I set Content-Type header to "application/json"

  Scenario: Test HEAD request
    When I make a HEAD request to "head"
    Then the response status should be "200"

  Scenario: Test GET request
    When I make a GET request to "get"
    Then the response status should be "200"

  Scenario: Test POST request
    When I make a POST request to "post"
    Then the response status should be "204"

  Scenario: Test POST request by checking we get the same JSON payload back
    When I make a POST request to "post/mirror"
    """
    {"title": "Some title", "nested": {"number": 42}, "array": [1, 2, 3]}
    """
    Then the response status should be "201"
    And the JSON should be
    """
    {"title": "Some title", "nested": {"number": 42}, "array": [1, 2, 3]}
    """

  Scenario: Test JSON path expection
    When I make a POST request to "post/mirror"
    """
    {"nested": {"number": 42}, "array": []}
    """
    Then the response status should be "201"
    And the JSON at path "nested" should be
    """
    {"number": 42}
    """

  Scenario: Test JSON array length calculation
    When I make a POST request to "post/mirror"
    """
    {"array": [1, 2, 3]}
    """
    Then the response status should be "201"
    Then the JSON array length at path "array" should be 3

  Scenario: Test storing item from JSON response in variable
    When I make a POST request to "post/mirror"
    """
    {"title": "Some title", "nested": {"number": 42}, "array": [1, 2, 3]}
    """
    Then the response status should be "201"
    When I store the JSON at path "nested" in "nested"
    Then the variable nested should be equal to JSON
    """
    {"number": 42}
    """
    And the variable nested should be equal to JSON {"number": 42}

  Scenario: Test OPTIONS request
    When I make an OPTIONS request to "options"
    Then the response status should be "200"
    And the Allow header should be "HEAD, GET, OPTIONS"

  Scenario: Test PUT request by checking we get the same revision back
    When I make a PUT request to "put"
    """
    {"rev": 2, "id": "foo"}
    """
    Then the response status should be "200"
    And the JSON at path "rev" should be 2

  Scenario: Test PATCH request
    When I make a PATCH request to "patch"
    """
    {"rev": 1}
    """
    Then the response status should be "200"
    And the JSON at path "rev" should be 1

  Scenario: Test DELETE request
    When I make a DELETE request to "delete"
    Then the response status should be "204"

  Scenario: Test TRACE request
    Given I set X-Foo header to "bar"
    When I make a TRACE request to "trace"
    Then the response status should be "200"
    And the response body should contain "X-Foo: bar"

  Scenario: Test GET request to URL with query string
    When I make a GET request to "get/args?foo=Some foo&bar=chocolate"
    Then the response status should be "200"
    And the JSON should be
    """
    {"foo": "Some foo", "bar": "chocolate"}
    """
