from urllib import urlencode

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode
    """

    if isinstance(params, dict):
        params = params.items()
    return urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])


def get_instance_from_path(path, *args, **kwargs):
    """
    Return an instance of a class, given the dotted
    Python import path (as a string) to the backend class.

    If the backend cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.

    """
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration backend %s: "%s"' % (module, e))
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration backend named "%s"' % (module, attr))

    return backend_class(*args, **kwargs)

