# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from glitter.models import Version, ContentBlock
from glitter.pages.models import Page

from .models import Redactor


class RedactorTestCase(TestCase):
    def setUp(self):
        page = Page.objects.create(url='/redactor/', title='Test page')

        self.page_content_type = ContentType.objects.get_for_model(Page)

        self.editor = User.objects.create_user(username='redactor', password='redactor')

        page_version = Version.objects.create(
            content_type=self.page_content_type, object_id=page.id,
            template_name='glitter/sample.html', owner=self.editor
        )
        self.redactor_block = Redactor.objects.create(
            content='Test'
        )

        self.content_block = ContentBlock.objects.create(
            obj_version=page_version,
            column='content',
            position=1,
            content_type=ContentType.objects.get_for_model(self.redactor_block),
            object_id=self.redactor_block.id
        )
        self.redactor_block.content_block = self.content_block
        self.redactor_block.save()

    def test_existance(self):
        redactor = Redactor.objects.get(id=self.redactor_block.id)
        self.assertEqual(redactor.id, self.redactor_block.id)
