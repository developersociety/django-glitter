import re

from django.contrib.syndication.views import add_domain
from django.template import RequestContext
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

    related_pages = block.relatedpage_set.select_related('page').all()
    related_pages_links = related_pages_generator(request, related_pages)

    return render_to_string((
        'glitter/blocks/%s.html' % (block._meta.model_name,),
    ), {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
        'related_pages': related_pages,
        'related_pages_links': related_pages_links,
    }, context_instance=RequestContext(request))
