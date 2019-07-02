def str_or_none(value):

    return value if value and isinstance(value, str) else None


def placeholder_file(filename, *_, **kwargs):

    with open(filename) as file:
        text = file.read()
        return text.format(**kwargs)
