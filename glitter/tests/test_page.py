# -*- coding: utf-8 -*-

import os

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, override_settings, modify_settings

from glitter.blocks.html.models import HTML
from glitter.models import Version, ContentBlock
from glitter.pages.models import Page


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sample',
    },
)
@override_settings(
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates'),),
)
class TestAdmin(TestCase):

    def setUp(self):
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

        self.html1_block = HTML.objects.create(content='<p>HTML Block</p>')
        self.html1_content_block = ContentBlock.objects.create(
            obj_version=self.page_version,
            column='main_content',
            position=1,
            content_type=ContentType.objects.get_for_model(self.html1_block),
            object_id=self.html1_block.id
        )
        self.html1_block.content_block = self.html1_content_block
        self.html1_block.save()

        # Information about model
        self.info = self.page._meta.app_label, self.page._meta.model_name

        self.html1_block_delete_url = reverse(
            'admin:%s_%s_block_delete' % self.info, args=(self.html1_content_block.id,)
        )
