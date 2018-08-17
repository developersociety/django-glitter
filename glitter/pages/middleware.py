import importlib
from threading import Lock
import sys

from django.http import Http404, HttpResponseRedirect

from glitter.exceptions import GlitterRedirectException, GlitterUnpublishedException
from glitter.pages.models import Page


class PageFallbackMiddleware(object):
    def process_response(self, request, response):

        # Import here as it causes migrations for pages if app is not installed apps.
        from glitter.pages.views import glitter, render_object_unpublished

        if response.status_code != 404:
            return response  # No need to check for a page for non-404 responses.

        try:
            return glitter(request=request, url=request.path_info)
        except Http404:
            # Return the original response if a 404 occurs
            return response
        except GlitterUnpublishedException as exception:
            return render_object_unpublished(request=request, obj=exception.obj)
        except GlitterRedirectException as exception:
            return HttpResponseRedirect(exception.url)

        return None


_urlconf_pages = []
_urlconf_lock = Lock()


class GlitterUrlConfMiddleware(object):
    def process_request(self, request):
        """
        Reloads glitter URL patterns if page URLs change.

        Avoids having to restart the server to recreate the glitter URLs being used by Django.
        """
        global _urlconf_pages

        page_list = list(
            Page.objects.exclude(glitter_app_name='').values_list('id', 'url').order_by('id')
        )

        with _urlconf_lock:
            if page_list != _urlconf_pages:
                glitter_urls = 'glitter.urls'
                if glitter_urls in sys.modules:
                    importlib.reload(sys.modules[glitter_urls])
                _urlconf_pages = page_list
