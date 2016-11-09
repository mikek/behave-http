Feature: HTTP requests
  As an imaginary HTTP API client
  I want to make sure HTTP steps do what they meant to do

  Background: Set target server address and headers
    Given I am using server "$TEST_SERVER"
    And I set base URL to "$TEST_URL"
    And I set "Accept" header to "application/json"
    And I set "Content-Type" header to "application/json"

  Scenario: Test getting context variable
    Given I set variable "foo" to "foo"
    Then the variable "foo" should be "foo"

  Scenario: Test HEAD request
    When I make a HEAD request to "head"
    Then the response status should be 200

  Scenario: Test GET request
    When I make a GET request to "get"
    Then the response status should be 200

  Scenario: Test GET request with full path
    When I make a GET request to "/different-prefix/get"
    Then the response status should be 200
    And the response body should contain "different prefix"

  Scenario: Test POST request
    When I make a POST request to "post"
    Then the response status should be 204

  Scenario: Test POST request by checking we get the same JSON payload back
    When I make a POST request to "post/mirror/json"
    """
    {"titlé": "Some titlé", "level1": {"number": 42}, "array": [1, 2, 3]}
    """
    Then the response status should be 201
    And the JSON should be
    """
    {"titlé": "Some titlé", "level1": {"number": 42}, "array": [1, 2, 3]}
    """

  Scenario: Test JSON path expection
    When I make a POST request to "post/mirror/json"
    """
    {"level1": {"level2": {"numbér": 42}}, "array": []}
    """
    Then the response status should be 201
    And the JSON at path "level1.level2" should be
    """
    {"numbér": 42}
    """

  Scenario: Test JSON array length calculation
    When I make a POST request to "post/mirror/json"
    """
    {"array": [1, 2, 3]}
    """
    Then the response status should be 201
    Then the JSON array length at path "array" should be 3

  Scenario: Test storing item from JSON response in variable
    When I make a POST request to "post/mirror/json"
    """
    {"title": "Some titlé", "level1": {"number": 42}, "array": [1, 2, 3]}
    """
    Then the response status should be 201
    When I store the JSON at path "level1" in "level1"
    Then the variable "level1" should be equal to JSON
    """
    {"number": 42}
    """
    And the variable "level1" should be equal to JSON {"number": 42}
    When I store the JSON at path "level1.number" in "number"
    Then the variable "number" should be equal to JSON 42
    When I store the JSON at path "title" in "title"
    Then the variable "title" should be equal to JSON "Some titlé"
    When I store the JSON at path "array" in "array"
    Then the variable "array" should be equal to JSON [1, 2, 3]

  Scenario: Test OPTIONS request
    When I make an OPTIONS request to "options"
    Then the response status should be 200
    And the "Allow" header should be "HEAD, GET, OPTIONS"

  Scenario: Test PUT request by checking we get the same revision back
    When I make a PUT request to "put/json"
    """
    {"rev": 2, "id": "foö"}
    """
    Then the response status should be 200
    And the JSON at path "rev" should be 2

  Scenario: Test PATCH request
    When I make a PATCH request to "patch/json"
    """
    {"rev": 1}
    """
    Then the response status should be 200
    And the JSON at path "rev" should be 1

  Scenario: Test DELETE request
    When I make a DELETE request to "delete"
    Then the response status should be 204

  Scenario: Test TRACE request
    Given I set "X-Foo" header to "bar"
    When I make a TRACE request to "trace"
    Then the response status should be 200
    And the response body should contain "X-Foo: bar"

  Scenario: Test GET request to URL with query string
    When I make a GET request to "get/args-to-json?foö=Some foö&bar=chocolate"
    Then the response status should be 200
    And the JSON should be
    """
    {"foö": "Some foö", "bar": "chocolate"}
    """

  Scenario: Test multiple expected response statuses
    When I make a HEAD request to "head"
    Then the response status should be one of "200, 204"

  Scenario: Test GET polling with checking for value that eventually succeeds
    When I keep sending GET requests to "get/poll" until JSON at path "counter" is
    """
    0
    """
    Then the response status should be 200

  Scenario: Test Basic Auth
    Given I set BasicAuth username to "test-user" and password to "test-password"
    When I make a GET request to "get/basic-auth"
    Then the response status should be 200

  Scenario: Test certificate is not verified
    Given I am using server "https://expired.identrustssl.com"
    And I do not want to verify server certificate
    When I make a GET request to "/"
    Then the response status should be 200
