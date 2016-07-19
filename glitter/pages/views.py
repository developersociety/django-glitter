# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from glitter.views import render_object_unpublished, render_page
from .models import Page


# Called from glitter.middleware.GlitterFallbackMiddleware
# Mostly a copy of the django.contrib.flatpages implementation
def glitter(request, url):
    PAGE_LOGIN_PERMS = getattr(settings, 'GLITTER_LOGIN_PERMS', False)

    if not url.startswith('/'):
        url = '/' + url

    page_opts = Page._meta.app_label, Page._meta.model_name

    query = {
        'url__exact': url
    }

    if hasattr(settings, 'PAGE_LANGUAGES'):
        PAGE_LANGUAGES = dict(settings.PAGE_LANGUAGES)
        split_url = list(filter(None, url.split('/')))
        language_code = split_url.pop(0)
        if language_code in PAGE_LANGUAGES:
            url = '/{}/'.format('/'.join(split_url))
            query['url__exact'] = url
            query['language'] = language_code

    try:
        page = get_object_or_404(
            Page.objects.select_related('current_version'), **query)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            page = get_object_or_404(Page, **query)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise

    # Unpublished page
    if not page.published or not page.current_version:
        return render_object_unpublished(request=request, obj=page)

    # Page with login required
    if page.login_required:
        def can_view_page(user):
            if PAGE_LOGIN_PERMS:
                # Need the 'view_protected_page' permission to access this page
                return (user.has_perm('%s.view_protected_%s' % page_opts) or
                        user.has_perm('%s.view_protected_%s' % page_opts, obj=page))
            else:
                # Any authenticated user will do
                return user.is_authenticated()

        @user_passes_test(can_view_page)
        def view_protected_page(request):
            return render_page(request, page, page.current_version)

        # Pass it to the protected version to see if the user can view the page
        return view_protected_page(request)

    return render_page(request, page, page.current_version)
