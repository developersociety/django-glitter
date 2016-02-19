# -*- coding: utf-8 -*-

import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.test import override_settings, modify_settings

from glitter.exceptions import GlitterRedirectException
from glitter.pages.models import Page
from glitter.models import Version
from glitter.page import Glitter


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sample',
    },
)
@override_settings(ROOT_URLCONF='glitter.tests.urls')
@override_settings(
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates'),),
    ROOT_URLCONF='glitter.tests.urls',
)
class TestExceptionsBase(TestCase):
    def setUp(self):
        User = get_user_model()

        # Page
        self.page = Page.objects.create(url='/test/', title='Test page')

        # Permissions
        self.edit_permissions = Permission.objects.get_by_natural_key(
            'edit_page', 'glitter_pages', 'page'
        )
        # Editor with editing permissions
        self.editor = User.objects.create_user('editor', 'editor@test.com', 'editor')
        self.editor.is_staff = True
        self.editor.user_permissions.add(self.edit_permissions)
        self.editor.save()
        self.editor_client = Client()
        self.editor_client.login(username='editor', password='editor')

        # Page version.
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page), object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor
        )
        self.glitter = Glitter(self.page_version)


class TestGlitterColumnException(TestExceptionsBase):
    def setUp(self):
        super(TestGlitterColumnException, self).setUp()

    def test_page_redirect_exception(self):
        url = '/'
        exception = GlitterRedirectException(url)
        self.assertEqual(exception.__str__(), 'Redirect to %s required' % (url,))
