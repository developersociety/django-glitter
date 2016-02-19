# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponseRedirect

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
