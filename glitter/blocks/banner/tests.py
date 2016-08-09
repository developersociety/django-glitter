# -*- coding: utf-8 -*-
from __future__ import unicode_literals

if __name__ == '__main__':
    import django
    django.setup()
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import get_callable, reverse
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test import modify_settings, override_settings

from glitter.models import Version, ContentBlock
from glitter.pages.models import Page

from glitter.blocks.banner.models import Banner, BannerBlock, BannerInline
from glitter.blocks.banner.admin import BannerInlineAdmin, BannerAdmin


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sample',
    },
)

@override_settings(
    ROOT_URLCONF='glitter.tests.urls',
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
        
        self.inline = BannerInline.objects.create(
            banner_block=self.banner_block, banner=self.banner)
        
        self.super_user = User.objects.create_superuser('test',
                                                        'test@test.com', 'test')
        self.super_user_client = Client()
        self.super_user_client.login(username='test', password='test')

    def test_view_without_block(self):
        self.view(
            None, self.request, False, self.content_block_without_obj, 'test-class'
        )

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
        response = self.super_user_client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_bannerblock_view_as_request(self):
        url = reverse('admin:glitter_banner_banner_change',
                      args=(self.banner.id,))
        response = self.super_user_client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_bannerblock_change(self):
        url = reverse('block_admin:glitter_banner_bannerblock_change',
                      args=(self.banner_block.id,))
        response = self.super_user_client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    from django.core.management import call_command
    call_command('test', 'glitter.blocks.banner.tests.BannerTestCase')