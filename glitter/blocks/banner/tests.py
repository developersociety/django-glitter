# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import get_callable, reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.test import modify_settings

from glitter.models import Version, ContentBlock
from glitter.pages.models import Page

from glitter.blocks.banner.models import Banner, BannerBlock, BannerInline
from glitter.blocks.banner.admin import BannerInlineAdmin


@modify_settings(INSTALLED_APPS={'append': 'glitter.tests.sample'})
class BannerTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(url='/redactor/', title='Test page')
        self.page_content_type = ContentType.objects.get_for_model(Page)

        editor = User.objects.create_superuser(
            username='editor', email='editor@example.org', password='editor',
        )
        self.client.login(username='editor', password='editor')

        page_version = Version.objects.create(
            content_type=self.page_content_type,
            object_id=self.page.id,
            template_name='glitter/sample.html',
            owner=editor,
        )

        self.factory = RequestFactory()

        self.banner = Banner.objects.create(
            title='Banner',
            link='www.blanc.ltd.uk'
        )
        self.banner_block = BannerBlock.objects.create()
        self.content_block = ContentBlock.objects.create(
            obj_version=page_version,
            column='main_content',
            position=1,
            content_type=ContentType.objects.get_for_model(BannerBlock),
            object_id=self.banner_block.id,
        )
        self.banner_block.content_block = self.content_block
        self.banner_block.save()

        self.request = self.factory.get('/')
        self.view = get_callable(BannerBlock.render_function)

        self.inline = BannerInline.objects.create(
            banner_block=self.banner_block, banner=self.banner)

    def test_view_with_block(self):
        self.view(
            self.banner_block, self.request, False, self.content_block, 'test-class'
        )

    def test_model_string(self):
        self.assertEqual(str(self.banner), 'Banner')
        self.assertEqual(str(self.inline), 'Banner')

    def test_view_inline(self):
        site = AdminSite()
        view = BannerInlineAdmin(self.request, site)
        field = self.inline._meta.get_field('banner')
        form_field = view.formfield_for_dbfield(field)
        self.assertTrue(len(list(form_field.choices)) > 1)

    def test_banner_view_as_request(self):
        url = reverse('admin:glitter_banner_banner_change',
                      args=(self.banner.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_bannerblock_view_as_request(self):
        url = reverse('admin:glitter_banner_banner_change',
                      args=(self.banner.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_bannerblock_change(self):
        url = reverse('block_admin:glitter_banner_bannerblock_change',
                      args=(self.banner_block.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
