from django.shortcuts import resolve_url

from .models import Page


def resolve_page(to, *args, **kwargs):
    """
    Resolve an object/string to a Page.

    The arguments could be:

        * A page: will be returned back immediately.

        * Any other model: the model's `get_absolute_url()` function will be
          called.

        * A view name, possibly with arguments: `urlresolvers.reverse()` will
          be used to reverse-resolve the name.

        * A URL string.

    For anything other than a page, a lookup is done on the URL of the object or
    view, and a Page is returned if it exists. If a page doesn't exist then
    it'll return None.
    """

    # Don't bother with a lookup if we're given None or an empty string
    if not to:
        return None

    try:
        return Page.objects.get(url=resolve_url(to, *args, **kwargs))
    except Page.DoesNotExist:
        pass

    return None
