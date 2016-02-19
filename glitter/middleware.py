from django.http import HttpResponseRedirect

from .exceptions import GlitterRedirectException, GlitterUnpublishedException
from .views import render_object_unpublished


class ExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, GlitterUnpublishedException):
            return render_object_unpublished(request=request, obj=exception.obj)

        if isinstance(exception, GlitterRedirectException):
            return HttpResponseRedirect(exception.url)

        return None
