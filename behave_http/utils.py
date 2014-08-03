from __future__ import unicode_literals
from functools import wraps
import jinja2
import os
from purl import URL


def _get_data_from_context(context):
    """Use context.text as a template and render against any stored state."""
    data = context.text if context.text else ''
    # Always clear the text to avoid accidental re-use.
    context.text = ''
    # NB rendering the template always returns unicode.
    result = jinja2.Template(data).render(context.template_data)
    return result.encode('utf8')


def dereference_step_parameters_and_data(f):
    """Decorator to dereference step parameters and data.

    This involves three steps:

        1) Rendering feature file step parameters as a Jinja2 template against
        context.template_data.

        2) Replacing step parameters with environment variable values if they
        look like an environment variable (start with a "$").

        3) Treating context.text as a Jinja2 template rendered against
        context.template_data, and putting the result in context.data.

    """
    @wraps(f)
    def wrapper(context, **kwargs):
        decoded_kwargs = {}
        for key, value in kwargs.items():
            value = jinja2.Template(value).render(context.template_data)
            if value.startswith('$'):
                value = os.environ.get(value[1:], '')
            decoded_kwargs[key] = value
        context.data = _get_data_from_context(context)
        return f(context, **decoded_kwargs)
    return wrapper


def append_path(url, url_path_segment):
    target = URL(url_path_segment)
    url = url.add_path_segment(target.path())
    if target.query():
        url = url.query(target.query())
    return url.as_string()
