# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import get_callable
from django.test import TestCase
from django.test.client import RequestFactory

from glitter.models import Version, ContentBlock
from glitter.pages.models import Page

from .models import ContactFormBlock


class FormTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(url='/form/', title='Test page')

        self.page_content_type = ContentType.objects.get_for_model(Page)

        self.editor = User.objects.create_user(username='form', password='form')

        page_version = Version.objects.create(
            content_type=self.page_content_type,
            object_id=self.page.id,
            template_name='glitter/sample.html',
            owner=self.editor
        )

        self.form_block = ContactFormBlock.objects.create(
            recipient='test@blanc.ltd.uk',
        )
        self.content_block = ContentBlock.objects.create(
            obj_version=page_version,
            column='side',
            position=1,
            content_type=ContentType.objects.get_for_model(ContactFormBlock),
            object_id=self.form_block.id,
        )
        self.form_block.content_block = self.content_block
        self.form_block.save()

        self.factory = RequestFactory()

        self.request = self.factory.get('/')
        self.view = get_callable(ContactFormBlock.render_function)

    def test_view_with_block(self):
        self.view(
            self.form_block, self.request, False, self.content_block, 'test-class'
        )
