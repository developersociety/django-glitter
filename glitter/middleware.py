# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect

from .exceptions import GlitterRedirectException, GlitterUnpublishedException
from .views import render_object_unpublished


class ExceptionMiddleware(object):
    """
    The middleware glitter.middleware.ExceptionMiddleware is handles exceptions if the object
    doesn’t have the current version or hasn’t been published it prompts the user to create a new
    page it also deals with blocks which raise exception.
    """

    def process_exception(self, request, exception):
        if isinstance(exception, GlitterUnpublishedException):
            return render_object_unpublished(request=request, obj=exception.obj)

        if isinstance(exception, GlitterRedirectException):
            return HttpResponseRedirect(exception.url)

        return None
