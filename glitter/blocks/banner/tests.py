# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import get_callable
from django.test import TestCase
from django.test.client import RequestFactory
from django.test import modify_settings

from glitter.models import Version, ContentBlock
from glitter.pages.models import Page


from .models import Banner, BannerBlock


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sample',
    },
)
class BannerTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.page = Page.objects.create(url='/redactor/', title='Test page')

        self.page_content_type = ContentType.objects.get_for_model(Page)

        self.editor = User.objects.create_user(username='banner', password='banner')

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
            content_type=ContentType.objects.get_for_model(BannerBlock),
        )
        self.content_block = ContentBlock.objects.create(
            obj_version=page_version,
            column='main_content',
            position=2,
            content_type=ContentType.objects.get_for_model(BannerBlock),
        )

        self.factory = RequestFactory()

        self.banner = Banner.objects.create(
            title='Banner',
            link='www.blanc.ltd.uk'
        )
        self.banner_block = BannerBlock.objects.create(
            content_block=self.content_block,
        )
        self.content_block.content_object = self.banner_block
        self.content_block.save()

        self.request = self.factory.get('/')
        self.view = get_callable(BannerBlock.render_function)

    def test_view_without_block(self):
        self.view(
            None, self.request, False, self.content_block_without_obj, 'test-class'
        )

    def test_view_with_block(self):
        self.view(
            self.banner_block, self.request, False, self.content_block, 'test-class'
        )