import os
from behave_http.environment import before_scenario  # noqa

default_env = {
    'TEST_SERVER': 'http://127.0.0.1:55080',
    'TEST_URL': 'test',
}


def before_all(context):
    for k, v in default_env.items():
        os.environ.setdefault(k, v)
