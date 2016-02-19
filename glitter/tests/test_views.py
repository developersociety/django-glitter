# -*- coding: utf-8 -*-

import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.test import TestCase, Client
from django.test import override_settings, modify_settings

from glitter.models import Version
from glitter.pages.models import Page


SAMPLE_BLOCK_MISSING = 'glitter.tests.sampleblocks' not in settings.INSTALLED_APPS


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sample',
    },
)
@override_settings(
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates'),),
    ROOT_URLCONF='glitter.tests.urls',
    GLITTER_LOGIN_PERMS=True,
)
class BaseViewCase(TestCase):

    def setUp(self):

        # Permissions
        self.edit_permissions = Permission.objects.get_by_natural_key(
            'edit_page', 'glitter_pages', 'page'
        )

        # Page
        self.page = Page.objects.create(url='/test/', title='Test page', published=True)

        # Page
        self.page_no_version = Page.objects.create(
            url='/test-12/', title='Test page', published=False
        )

        # Page
        self.page_no_first_slash = Page.objects.create(
            url='test/', title='Test page', published=True
        )
        self.page_no_ending_slash = Page.objects.create(
            url='/test', title='Test page', published=True
        )

        self.page_testing = Page.objects.create(
            url='/testing/', title='Test page', published=True
        )

        User = get_user_model()
        # Editor with editing permissions
        self.editor = User.objects.create_user('editor', 'editor@test.com', 'editor')
        self.editor.is_staff = True
        self.editor.user_permissions.add(self.edit_permissions)
        self.editor.save()
        self.editor_client = Client()
        self.editor_client.login(username='editor', password='editor')

        # Editor with not editing permissions
        self.editor_no_permissions = User.objects.create_user(
            'editor_no_perm', 'editor_no_perm@test.com', 'editor_no_perm'
        )
        self.editor_no_permissions.save()
        self.editor_no_permissions_client = Client()

        # Page version.
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page), object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor,
            version_number=1
        )

        self.page.current_version = self.page_version
        self.page.save()


class TestGlitterView(BaseViewCase):

    def setUp(self):
        super(TestGlitterView, self).setUp()

    def test_existing_page(self):
        """Test normal page."""
        response = self.editor_no_permissions_client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

    def test_page_with_no_first_slash(self):
        """Test make sure add slash in front."""
        response = self.editor_no_permissions_client.get(self.page_no_first_slash.url)
        self.assertEqual(response.status_code, 200)

    def test_page_with_no_ending_slash(self):
        """Test if url with no ending slash."""
        response = self.editor_no_permissions_client.get('/testing')
        self.assertEqual(response.status_code, 301)

    @override_settings(
        APPEND_SLASH=False
    )
    def test_page_does_not_exist(self):
        """Test if url with no ending slash."""
        response = self.editor_no_permissions_client.get('/testi2')
        self.assertEqual(response.status_code, 404)

    def test_page_unpublished(self):
        """Test if url with no ending slash."""
        self.page.published = False
        self.page.save()

        # User with permissions
        response = self.editor_client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

        # No permissions
        response = self.editor_no_permissions_client.get(self.page.url)
        self.assertEqual(response.status_code, 404)

    def test_page_login_required(self):
        self.page.login_required = True
        self.page.save()

        response = self.editor_client.get(self.page.url)
        self.assertEqual(response.status_code, 302)

    @override_settings(GLITTER_LOGIN_PERMS=False)
    def test_page_login_required_with_login_perms(self):
        self.page.login_required = True
        self.page.save()

        with self.settings(GLITTER_LOGIN_PERMS=False):
            response = self.editor_client.get(self.page.url)
            self.assertEqual(response.status_code, 200)


class TestRenderPageUnpublished(BaseViewCase):

    def setUp(self):
        super(TestRenderPageUnpublished, self).setUp()

    def test_exceptionssasd(self):
        response = self.editor_client.get(self.page_no_version.url)
        self.assertEqual(response.status_code, 200)
