# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re

from django.contrib.syndication.views import add_domain
from django.template.loader import render_to_string


def related_pages_generator(request, related_pages):
    for related_page in related_pages:
        if related_page.page:
            page_url = related_page.page.get_absolute_url()
            url = add_domain(request.get_host(), page_url, secure=request.is_secure())
        else:
            url = related_page.link

        # Remove common prefix
        url = re.sub(r'^https?://(?:www\.)?', '', url, flags=re.IGNORECASE)

        # Remove common suffix
        if url.endswith('/'):
            url = url.rstrip('/')

        yield related_page, url


def relatedpages_view(block, request, rerender, content_block, block_classes):
    css_classes = ' '.join(block_classes)
    related_pages = None

    if block:
        related_pages = block.relatedpage_set.select_related('page').all()
    related_pages_links = related_pages_generator(request, related_pages)

    template_name = 'glitter/blocks/%s.html' % content_block.content_type.model
    context = {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
        'related_pages': related_pages,
        'related_pages_links': related_pages_links}
    rendered = render_to_string(template_name, context, request=request)
    return rendered
