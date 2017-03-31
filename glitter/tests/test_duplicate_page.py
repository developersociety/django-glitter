# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.test import override_settings

from glitter.blocks.html.models import HTML
from glitter.models import ContentBlock, Version
from glitter.pages.models import Page


@override_settings(
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates'),),
    GLITTER_SHOW_LOGIN_REQUIRED=True,
)
class DuplicatePageTestCase(TestCase):
    def setUp(self):

        # Page
        self.page = Page.objects.create(url='/test/', title='Test page')

        # User
        self.super_user = User.objects.create_superuser('test', 'test@test.com', 'test')
        self.super_user_client = Client()
        self.super_user_client.login(username='test', password='test')

        # Page version.
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page), object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.super_user
        )

        # Html block
        self.html_block = HTML.objects.create(content='<p>HTML Block</p>')
        self.content_block = ContentBlock.objects.create(
            obj_version=self.page_version,
            column='main_content',
            position=1,
            content_type=ContentType.objects.get_for_model(self.html_block),
            object_id=self.html_block.id
        )
        self.html_block.content_block = self.content_block
        self.html_block.save()

        self.duplicate_page_view_url = reverse(
            'admin:glitter_pages_page_duplicate', args=(self.page.id,)
        )

    def test_duplication(self):
        data = {
            'url': '/newhome/',
            'title': 'Title'
        }
        self.super_user_client.post(self.duplicate_page_view_url, data)
        self.assertEqual(data['url'], Page.objects.get(url=data['url']).url)
