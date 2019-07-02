import os
from .settings import TEMPLATED_DIR


def str_or_none(value):

    return value if value and isinstance(value, str) else None


def placeholder_template(template_name, *_, **kwargs):

    filename = os.path.join(TEMPLATED_DIR, template_name)

    with open(filename) as file:
        text = file.read()
        return text.format(**kwargs)
