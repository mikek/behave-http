"""Reasonably complete set of BDD steps for testing a simple HTTP service.

Some state is set-up and shared between steps using the context variable. It is
reset at the start of every scenario by environment.before_scenario.

"""
from __future__ import unicode_literals
import behave
import jpath
import json
from ensure import ensure
from purl import URL
import requests
import time

from behave_http.utils import dereference_step_parameters_and_data, append_path


@behave.given('I am using server "{server}"')
@dereference_step_parameters_and_data
def using_server(context, server):
    context.server = URL(server)


@behave.given('I set base URL to "{base_url}"')
@dereference_step_parameters_and_data
def set_base_url(context, base_url):
    context.server = context.server.add_path_segment(base_url)


@behave.given('I set "{var}" header to "{value}"')
@dereference_step_parameters_and_data
def set_header(context, var, value):
    # We must keep the headers as implicit ascii to avoid encoding failure when
    # the entire HTTP body is constructed by concatenating strings.
    context.headers[var.encode('ascii')] = value.encode('ascii')


@behave.given(
    'I set BasicAuth username to "{username}" and password to "{password}"')
@dereference_step_parameters_and_data
def set_basic_auth_headers(context, username, password):
    context.auth = (username, password)


@behave.given('I use query OAuth with key="{key}" and secret="{secret}"')
@dereference_step_parameters_and_data
def query_oauth(context, key, secret):
    context.auth = requests.auth.OAuth1(
        key, secret, signature_type='query')


@behave.given('I use header OAuth with key="{key}" and secret="{secret}"')
@dereference_step_parameters_and_data
def header_oauth(context, key, secret):
    context.auth = requests.auth.OAuth1(
        key, secret, signature_type='auth_header')


@behave.given('I set variable "{variable}" to {value}')
@dereference_step_parameters_and_data
def set_var(context, variable, value):
    setattr(context, variable, json.loads(value))


@behave.when(
    'I keep sending GET requests to "{url_path_segment}" until JSON at path '
    '"{jsonpath}" is')
@dereference_step_parameters_and_data
def poll_GET(context, url_path_segment, jsonpath):
    json_value = json.loads(context.data.decode('utf-8'))
    url = append_path(context.server, url_path_segment)
    for i in range(context.n_attempts):
        response = requests.get(
            url, headers=context.headers, auth=context.auth)
        if jpath.get(jsonpath, response.json()) == json_value:
            context.response = response
            return
        time.sleep(context.pause_between_attempts)
    raise AssertionError(
        'Condition not met after %d attempts' %
        context.n_attempts)  # pragma: no cover


@behave.when('I make a HEAD request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def head_request(context, url_path_segment):
    url = append_path(context.server, url_path_segment)
    context.response = requests.head(
        url, headers=context.headers, auth=context.auth)


@behave.when('I make an OPTIONS request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def options_request(context, url_path_segment):
    url = append_path(context.server, url_path_segment)
    context.response = requests.options(
        url, headers=context.headers, auth=context.auth)


@behave.when('I make a TRACE request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def trace_request(context, url_path_segment):
    url = append_path(context.server, url_path_segment)
    context.response = requests.request(
        'TRACE', url, headers=context.headers, auth=context.auth)


@behave.when('I make a PATCH request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def patch_request(context, url_path_segment):
    url = append_path(context.server, url_path_segment)
    context.response = requests.patch(
        url, data=context.data, headers=context.headers, auth=context.auth)


@behave.when('I make a PUT request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def put_request(context, url_path_segment):
    url = append_path(context.server, url_path_segment)
    context.response = requests.put(
        url, data=context.data, headers=context.headers, auth=context.auth)


@behave.when('I make a POST request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def post_request(context, url_path_segment):
    url = append_path(context.server, url_path_segment)
    context.response = requests.post(
        url, data=context.data, headers=context.headers, auth=context.auth)


@behave.when('I make a GET request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def get_request(context, url_path_segment):
    url = append_path(context.server, url_path_segment)
    context.response = requests.get(
        url, headers=context.headers, auth=context.auth)


@behave.when('I make a DELETE request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def delete_request(context, url_path_segment):
    url = append_path(context.server, url_path_segment)
    context.response = requests.delete(
        url, headers=context.headers, auth=context.auth)


@behave.when('I store the JSON at path "{jsonpath}" in "{variable}"')
@dereference_step_parameters_and_data
def store_for_template(context, jsonpath, variable):
    context.template_data[variable] = jpath.get(
        jsonpath, context.response.json())


@behave.then('the variable "{variable}" should be "{value}"')
@dereference_step_parameters_and_data
def get_var(context, variable, value):
    ensure(getattr(context, variable)).equals(value)


@behave.then('the response status should be one of "{statuses}"')
@dereference_step_parameters_and_data
def response_status_in(context, statuses):
    ensure(context.response.status_code).is_in(
        [int(s) for s in statuses.split(',')])


@behave.then('the response status should be {status}')
@dereference_step_parameters_and_data
def response_status(context, status):
    ensure(context.response.status_code).equals(int(status))


@behave.then('the response body should contain "{content}"')
@dereference_step_parameters_and_data
def response_body_contains(context, content):
    ensure(content).is_in(context.response.content.decode('utf-8'))


@behave.then('the "{var}" header should be "{value}"')
@dereference_step_parameters_and_data
def check_header_inline(context, var, value):
    ensure(context.response.headers[var].encode('ascii')).equals(
        value.encode('ascii'))


@behave.then('the JSON should be')
@dereference_step_parameters_and_data
def json_should_be(context):
    ensure(context.response.json()).equals(
        json.loads(context.data.decode('utf-8')))


@behave.then('the JSON array length at path "{jsonpath}" should be {value}')
@dereference_step_parameters_and_data
def json_array_len_at_path_inline(context, jsonpath, value):
    length = int(json.loads(value))
    ensure(jpath.get(jsonpath, context.response.json())).has_length(length)


@behave.then('the JSON at path "{jsonpath}" should be {value}')
@dereference_step_parameters_and_data
def json_at_path_inline(context, jsonpath, value):
    json_value = json.loads(value)
    ensure(jpath.get(jsonpath, context.response.json())).equals(json_value)


@behave.then('the JSON at path "{jsonpath}" should be')
@dereference_step_parameters_and_data
def json_at_path(context, jsonpath):
    ensure(jpath.get(jsonpath, context.response.json())).equals(
        json.loads(context.data.decode('utf-8')))


@behave.then('the variable "{variable}" should be equal to JSON')
@dereference_step_parameters_and_data
def get_context_var_json_value(context, variable):
    ensure(context.template_data[variable]).equals(
        json.loads(context.data.decode('utf-8')))


@behave.then('the variable "{variable}" should be equal to JSON {value}')
@dereference_step_parameters_and_data
def get_context_var_json_value_inline(context, variable, value):
    ensure(context.template_data[variable]).equals(json.loads(value))
