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
)
class TestAdmin(TestCase):

    def setUp(self):

        # Permissions
        self.edit_permissions = Permission.objects.get_by_natural_key(
            'edit_page', 'glitter_pages', 'page'
        )

        # Page
        self.page = Page.objects.create(url='/test/', title='Test page', published=True)

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

    def test_glitter_head(self):
        """Test as front-end user to see if controllers are shown."""

        response = self.editor_no_permissions_client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

        response = self.editor_client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
