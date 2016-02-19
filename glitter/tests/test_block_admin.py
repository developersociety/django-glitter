# -*- coding: utf-8 -*-

from unittest import skipIf

from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.test import override_settings, modify_settings

from glitter.block_admin import BlockAdminSite, BlockModelAdmin
from glitter.blocks.html.models import HTML
from glitter.pages.admin import PageAdmin
from glitter.pages.models import Page
from glitter.models import ContentBlock, Version


SAMPLE_BLOCK_MISSING = 'glitter.tests.sampleblocks' not in settings.INSTALLED_APPS
if not SAMPLE_BLOCK_MISSING:
    from glitter.tests.sampleblocks.admin import SampleInlineAdmin


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sampleblocks',
    },
)
@override_settings(ROOT_URLCONF='glitter.tests.urls')
@override_settings(
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
)
class TestBlockAdminSite(TestCase):
    def setUp(self):
        self.site = BlockAdminSite(name='block_admin')
        self.site.register(HTML)

        self.page_admin = PageAdmin(Page, AdminSite())

        User = get_user_model()
        # Superuser
        self.super_user = User.objects.create_superuser('test', 'test@test.com', 'test')
        self.super_user_client = Client()
        self.super_user_client.login(username='test', password='test')

        # Normal user
        self.normal_user = User.objects.create_user('name', 'test1@test.com', 'psw')
        self.normal_user_client = Client()
        self.normal_user_client.login(username='name', password='psw')

    def test_register_with_admin_class(self):
        self.site.unregister(HTML)
        self.site.register(HTML, BlockModelAdmin)

    def test_register_block(self):
        self.site.register_block(HTML, 'Common')

        # Run again whe `Common` is added in self.block_list
        self.site.register_block(HTML, 'Common')

    def test_get_urls(self):
        with self.settings(DEBUG=True):
            self.site.get_urls()
        self.site.get_urls()

    def test_admin_view(self):
        # Cacheble
        jsi18n_url = reverse('block_admin:jsi18n')
        response = self.super_user_client.get(jsi18n_url)
        self.assertEqual(response.status_code, 200)

        # Not cacheble
        jsi18n_url = reverse('block_admin:jsi18n')
        response = self.super_user_client.get(jsi18n_url, {'cacheable': False})
        self.assertEqual(response.status_code, 200)

        response = self.normal_user_client.get(jsi18n_url)
        self.assertEqual(response.status_code, 403)


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sampleblocks',
    },
)
@override_settings(ROOT_URLCONF='glitter.tests.urls')
class TestBlockModelAdmin(TestCase):
    def setUp(self):

        User = get_user_model()
        # Superuser
        self.superuser = User.objects.create_superuser('test', 'test@test.com', 'test')
        self.superuser_client = Client()
        self.superuser_client.login(username='test', password='test')

        # Normal user
        self.normal_user = User.objects.create_user('name', 'test1@test.com', 'psw')
        self.normal_user.is_staff = True
        self.normal_user.save()
        self.normal_user_client = Client()
        self.normal_user_client.login(username='name', password='psw')

        # Page
        self.page = Page.objects.create(url='/test/', title='Test page')

        # Page version.
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page), object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.superuser
        )
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

        self.site = AdminSite()
        self.model_admin = BlockModelAdmin(HTML, self.site)

        # Information about model
        self.info = self.model_admin.model._meta.app_label, self.model_admin.model._meta.model_name

        self.continue_view_url = reverse(
            'block_admin:%s_%s_continue' % self.info, args=(self.html_block.id,)
        )

        self.change_view_url = reverse(
            'block_admin:%s_%s_change' % self.info, args=(self.html_block.id,)
        )

    def test_change_form_template(self):
        self.model_admin.change_form_template

    def test_admin_view(self):
        jsi18n_url = reverse('block_admin:jsi18n')
        response = self.superuser_client.get(jsi18n_url)
        self.assertEqual(response.status_code, 200)

    def test_continue_view(self):
        response = self.superuser_client.get(self.continue_view_url)
        self.assertEqual(response.status_code, 200)

        continue_view_url_does_not_exit = reverse(
            'block_admin:%s_%s_continue' % self.info, args=('4')
        )
        response = self.superuser_client.get(continue_view_url_does_not_exit)
        self.assertEqual(response.status_code, 404)

    def test_continue_view_permissions(self):
        # Permission denied as user doesn't have permissions
        response = self.normal_user_client.get(self.continue_view_url)
        self.assertEqual(response.status_code, 403)

    def test_change_view(self):
        response = self.superuser_client.get(self.change_view_url)
        self.assertEqual(response.status_code, 200)

    def test_change_view_permissions(self):
        # Permission denied as user doesn't have permissions
        response = self.normal_user_client.get(self.change_view_url)
        self.assertEqual(response.status_code, 403)

        change_view_url_does_not_exit = reverse(
            'block_admin:%s_%s_change' % self.info, args=('4')
        )
        response = self.superuser_client.get(change_view_url_does_not_exit)
        self.assertEqual(response.status_code, 404)

    def test_change_view_page_version(self):
        self.page_version.version_number = 1
        self.page_version.save()
        response = self.superuser_client.get(self.change_view_url)
        self.assertEqual(response.status_code, 403)

    def test_response_change(self):
        """Test response change with and without _continue post."""
        opts = self.html_block._meta.app_label, self.html_block._meta.model_name
        cat = reverse('block_admin:%s_%s_change' % opts, args=(self.html_block.id,))
        response = self.superuser_client.post(cat, {
            'content': '<h1>Test</h1>',
            '_continue': True,
        })
        self.assertEqual(response.status_code, 302)
        response = self.superuser_client.post(cat, {
            'content': '<h1>Test</h1>',
        })
        self.assertEqual(response.status_code, 200)


@skipIf(SAMPLE_BLOCK_MISSING, 'glitter.tests.sampleblocks is not installed')
class TestInlineBlockModelAdmin(TestCase):
    def setUp(self):
        # Superuser
        User = get_user_model()
        self.superuser = User.objects.create_superuser('test', 'test@test.com', 'test')
        self.superuser_client = Client()
        self.superuser_client.login(username='test', password='test')

        self.model_admin = SampleInlineAdmin(Page, AdminSite())

    def test_has_add_permission(self):
        request = MockRequest()
        request.user = self.superuser
        self.assertTrue(self.model_admin.has_add_permission(request))

    def test_has_change_permission(self):
        request = MockRequest()
        request.user = self.superuser
        self.assertTrue(self.model_admin.has_change_permission(request))

    def test_has_delete_permission(self):
        request = MockRequest()
        request.user = self.superuser
        self.assertTrue(self.model_admin.has_delete_permission(request))
