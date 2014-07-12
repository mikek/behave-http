import decorator
import jinja2
import os
from purl import URL


def _decode_parameter(value):
    """Get BDD step parameter, redirecting to env var if start with $."""
    if value.startswith('$'):
        return os.environ.get(value[1:], '')
    else:
        return value


def _render_parameters_with_context(context, params):
    rendered_params = []
    for param in params:
        rendered_params.append(
            jinja2.Template(param).render(context.template_data))
    return rendered_params


def _get_data_from_context(context):
    """Use context.text as a template and render against any stored state."""
    data = context.text if context.text else u''
    # Always clear the text to avoid accidental re-use.
    context.text = u''
    # NB rendering the template always returns unicode.
    result = jinja2.Template(data).render(context.template_data)
    return result.encode('utf8')


@decorator.decorator
def dereference_step_parameters_and_data(f, context, *params):
    """Decorator to dereference step parameters and data.

    This involves three steps:

        1) Rendering feature file step parameters as a Jinja2 template against
        context.template_data.

        2) Replacing step parameters with environment variable values if they
        look like an environment variable (start with a "$").

        3) Treating context.text as a Jinja2 template rendered against
        context.template_data, and putting the result in context.data.

    """
    rendered_params = _render_parameters_with_context(context, params)
    decoded_params = map(_decode_parameter, rendered_params)
    context.data = _get_data_from_context(context)
    f(context, *decoded_params)


def append_path(url, url_path_segment):
    target = URL(url_path_segment)
    url = url.add_path_segment(target.path())
    if target.query():
        url = url.query(target.query())
    return url.as_string()
