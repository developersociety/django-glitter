# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.test import override_settings

from glitter.pages.models import Page
from glitter.models import Version


@override_settings(ROOT_URLCONF='glitter.tests.urls')
@override_settings(PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',))
class TestListeners(TestCase):
    def setUp(self):
        # Page
        self.page = Page.objects.create(url='/test/', title='Test page')

        User = get_user_model()
        # Superuser
        self.superuser = User.objects.create_superuser('test', 'test@test.com', 'test')
        self.superuser_client = Client()
        self.superuser_client.login(username='test', password='test')

        # Page version.
        self.page_version = Version.objects.create(
            page=self.page, template_name='glitter/sample.html', owner=self.superuser
        )
