# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import get_callable
from django.test import TestCase
from django.test.client import RequestFactory

from glitter.models import Version, ContentBlock
from glitter.pages.models import Page

from .models import ContactFormBlock


class FormTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.page = Page.objects.create(url='/form/', title='Test page')

        self.page_content_type = ContentType.objects.get_for_model(Page)

        self.editor = User.objects.create_user(username='form', password='form')

        page_version = Version.objects.create(
            content_type=self.page_content_type,
            object_id=self.page.id,
            template_name='glitter/sample.html',
            owner=self.editor
        )
        self.content_block_without_obj = ContentBlock.objects.create(
            obj_version=page_version,
            column='main_content',
            position=1,
            content_type=ContentType.objects.get_for_model(ContactFormBlock),
        )
        self.content_block = ContentBlock.objects.create(
            obj_version=page_version,
            column='side',
            position=1,
            content_type=ContentType.objects.get_for_model(ContactFormBlock),
        )
        self.factory = RequestFactory()

        self.form_block = ContactFormBlock.objects.create(
            recipient='test@blanc.ltd.uk',
        )
        self.content_block.content_object = self.form_block
        self.content_block.save()

        self.request = self.factory.get('/')
        self.view = get_callable(ContactFormBlock.render_function)

    def test_view_without_block(self):
        self.view(
            None, self.request, False, self.content_block_without_obj, 'test-class',
            ContactFormBlock.form_class
        )

    def test_view_with_block(self):
        self.view(
            self.form_block, self.request, False, self.content_block, 'test-class'
        )
