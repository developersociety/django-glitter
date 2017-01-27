# -*- coding: utf-8 -*-

import importlib

from django.conf import settings
from django.http import Http404, HttpResponseRedirect

from glitter import urls as glitter_urls
from glitter.exceptions import GlitterRedirectException, GlitterUnpublishedException


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


class GlitterUrlConf(object):
    def __init__(self):
        """
        URLs for Glitter App Pages can change based upon user's actions. So need to rebuild on each
        request.

        Have tried to reload the minimum amount of urlconfs to keep performance up.
        """
        root_urlconf = importlib.import_module(settings.ROOT_URLCONF)
        importlib.reload(root_urlconf)
        importlib.reload(glitter_urls)
        self.urlpatterns = root_urlconf.urlpatterns


class GlitterUrlConfMiddleware(object):
    def process_request(self, request):
        """
        Avoids having to restart the server to recreate the url_conf being used by Django.

        Doing it this way allows the url_conf to be set at runtime.
        """
        request.urlconf = GlitterUrlConf()
