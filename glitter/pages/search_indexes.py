# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.six.moves import html_parser

from haystack import indexes

from glitter.page import Glitter
from glitter.pages.models import Page


class PageCharField(indexes.CharField):
    def prepare_template(self, obj):
        template_name = 'search/indexes/%s/%s_%s.txt' % (
            obj._meta.app_label, obj._meta.model_name, self.instance_name)

        # Need to fake an HTTP request incase any templates aren't happy
        try:
            server_name = getattr(settings, 'ALLOWED_HOSTS', '127.0.0.1')[0]
        except IndexError:
            server_name = '127.0.0.1'

        request = HttpRequest()
        request.META = {
            'SERVER_NAME': server_name,
            'SERVER_PORT': 80,
        }
        request.path = request.path_info = obj.get_absolute_url()
        request.method = 'GET'
        request.user = AnonymousUser()

        # Create Glitter to render
        current_version = obj.current_version
        glitter = Glitter(page_version=current_version, request=request)

        # Render the template into a variable
        columns = glitter.render()
        content = render_to_string(template_name, {
            'glitter': glitter,
            'edit_mode': False,
            'columns': columns,
            obj._meta.model_name: obj,
            'object': obj,
        }, context_instance=RequestContext(request))

        # Need to escape HTML entities
        htmlparser = html_parser.HTMLParser()
        unescape = htmlparser.unescape
        content = unescape(content)

        # Prune excessive whitespace
        content = re.sub(r'\s+', ' ', content, flags=re.MULTILINE)

        return content


class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = PageCharField(document=True, use_template=True)

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            published=True, current_version__isnull=False
        ).exclude(
            login_required=True
        )
