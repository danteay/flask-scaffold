"""Global app context"""

# pylint: disable=invalid-name
# pylint: disable=global-statement

context = {}


def set_value(key, value):
    """
    set Key value to the context var
    :param key:
    :param value:
    :return: None
    """

    global context
    context.update({key: value})


def get_value(key):
    """
    Return a stored value in the global context
    :param key: Name of the key
    :return: Stored value
    """

    global context
    return context.get(key, None)


def delete(key):
    """
    Delete some context key
    :param key:
    """
    global context

    if key in context:
        del context[key]


def reset():
    """Reset the global context values"""
    global context
    context.clear()
