# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import get_callable
from django.test import TestCase
from django.test.client import RequestFactory
from django.test import modify_settings

from glitter.models import Version, ContentBlock
from glitter.pages.models import Page


from .models import RelatedPagesBlock


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sample',
    },
)
class RelatedPageTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(url='/related-page/', title='Test page')

        self.page_content_type = ContentType.objects.get_for_model(Page)

        self.editor = User.objects.create_user(username='relatedpage', password='relatedpage')

        page_version = Version.objects.create(
            content_type=self.page_content_type,
            object_id=self.page.id,
            template_name='glitter/sample.html',
            owner=self.editor
        )

        self.factory = RequestFactory()

        self.related_page_block = RelatedPagesBlock.objects.create()
        self.content_block = ContentBlock.objects.create(
            obj_version=page_version,
            column='main_content',
            position=1,
            content_type=ContentType.objects.get_for_model(RelatedPagesBlock),
            object_id=self.related_page_block.id,
        )

        self.related_page_block.content_block = self.content_block
        self.related_page_block.save()

        self.request = self.factory.get('/')
        self.view = get_callable(RelatedPagesBlock.render_function)

    def test_view_with_block(self):
        self.view(
            self.related_page_block, self.request, False, self.content_block, 'test-class'
        )
