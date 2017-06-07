# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase, Client
from django.test import override_settings, modify_settings

from glitter.forms import MoveBlockForm
from glitter.blocks.html.models import HTML
from glitter.models import Version, ContentBlock
from glitter.pages.admin import PageAdmin
from glitter.pages.models import Page
from glitter.tests.sample.models import Book


SAMPLE_BLOCK_MISSING = 'glitter.tests.sampleblocks' not in settings.INSTALLED_APPS


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sample',
    },
)
@override_settings(
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates'),),
    GLITTER_SHOW_LOGIN_REQUIRED=True,
)
class TestAdmin(TestCase):

    def setUp(self):

        # Permissions
        self.edit_permissions = Permission.objects.get_by_natural_key(
            'edit_page', 'glitter_pages', 'page'
        )

        # Page
        self.page = Page.objects.create(url='/test/', title='Test page')

        # Information about model
        self.info = self.page._meta.app_label, self.page._meta.model_name

        # Superuser
        self.super_user = User.objects.create_superuser('test', 'test@test.com', 'test')
        self.super_user_client = Client()
        self.super_user_client.login(username='test', password='test')

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
        self.editor_no_permissions.is_staff = True
        self.editor_no_permissions.save()
        self.editor_no_permissions_client = Client()
        self.editor_no_permissions_client.login(
            username='editor_no_perm', password='editor_no_perm'
        )

        # Page version.
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page), object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor
        )

        self.page_admin = PageAdmin(Page, AdminSite())

        self.change_obj_url = reverse('admin:glitter_pages_page_change', args=(self.page.id,))
        self.add_obj_url = reverse('admin:glitter_pages_page_add')
        self.page_redirect_url = reverse('admin:glitter_pages_page_redirect', args=(self.page.id,))

    def test_data_for_change_and_add_response(self):
        response_data = {'url': '/testing2/', 'title': 'Testing2'}
        response_save_and_edit_data = {
            'url': '/testing223/', 'title': 'Testing2', '_saveandedit': True
        }
        response_save_and_continue_edit = {
            'url': '/testing223/', 'title': 'Testing2', '_continue': True
        }
        return response_data, response_save_and_edit_data, response_save_and_continue_edit

    def test_admin_url(self):
        self.page_admin.view_url(self.page)

    def test_unpublish_count(self):
        self.page_admin.admin_unpublished_count(self.page)


@modify_settings(
    INSTALLED_APPS={
        'append': 'glitter.tests.sample',
    },
)
class TestPermissions(TestCase):
    def setUp(self):
        # Permissions for objects we're testing
        self.edit_page = Permission.objects.get_by_natural_key(
            'edit_page', 'glitter_pages', 'page'
        )
        self.publish_page = Permission.objects.get_by_natural_key(
            'publish_page', 'glitter_pages', 'page'
        )
        self.edit_book = Permission.objects.get_by_natural_key(
            'edit_book', 'sample', 'book'
        )
        self.publish_book = Permission.objects.get_by_natural_key(
            'publish_book', 'sample', 'book'
        )

        # Superuser
        self.superuser = User.objects.create_superuser(
            username='superuser', email='', password=None
        )

        # Editor with editing permissions
        self.editor = User.objects.create_user(username='editor', email='', password=None)
        self.editor.is_staff = True
        self.editor.save()
        self.editor.user_permissions.add(self.edit_page, self.edit_book)

        # Publisher with edit and publish permissions
        self.publisher = User.objects.create_user(username='publisher', email='', password=None)
        self.publisher.is_staff = True
        self.publisher.save()
        self.publisher.user_permissions.add(
            self.edit_page, self.publish_page, self.edit_book, self.publish_book
        )

        # Staff with no editing permissions
        self.staff = User.objects.create_user(username='staff', email='', password=None)
        self.staff.is_staff = True
        self.staff.save()

        # Page with an unsaved page version
        self.page = Page.objects.create(url='/test/', title='Test page')
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page),
            object_id=self.page.id,
            template_name='glitter/sample.html',
            owner=self.editor,
        )
        self.page_admin = PageAdmin(Page, AdminSite())

        # Sample model
        self.book = Book.objects.create(title='Hello')
        self.book_admin = PageAdmin(Book, AdminSite())

    def test_edit_permission(self):
        # Only people with glitter_pages.edit_page have edit permission
        request = HttpRequest()

        request.user = self.editor
        self.assertTrue(self.page_admin.has_edit_permission(request=request))

        request.user = self.staff
        self.assertFalse(self.page_admin.has_edit_permission(request=request))

    def test_edit_version(self):
        # Only the creator of an unsaved version can edit it
        request = HttpRequest()

        request.user = self.superuser
        self.assertFalse(self.page_admin.has_edit_permission(
            request=request, version=self.page_version
        ))

        request.user = self.editor
        self.assertTrue(self.page_admin.has_edit_permission(
            request=request, version=self.page_version
        ))

    def test_publish_permission(self):
        # Only people with glitter_pages.publish_page have publish permission
        request = HttpRequest()

        request.user = self.publisher
        self.assertTrue(self.page_admin.has_publish_permission(request=request))

        request.user = self.staff
        self.assertFalse(self.page_admin.has_publish_permission(request=request))

    def test_book_model(self):
        # Test that permissions work with different types of models
        request = HttpRequest()

        request.user = self.editor
        self.assertTrue(self.book_admin.has_edit_permission(request=request))

        request.user = self.publisher
        self.assertTrue(self.book_admin.has_publish_permission(request=request))

        request.user = self.staff
        self.assertFalse(self.book_admin.has_edit_permission(request=request))
        self.assertFalse(self.book_admin.has_publish_permission(request=request))


class BaseViewsCase(TestAdmin):

    def setUp(self):
        super(BaseViewsCase, self).setUp()

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

        self.html2_block = HTML.objects.create(content='<p>HTML Block</p>')
        self.html2_content_block = ContentBlock.objects.create(
            obj_version=self.page_version,
            column='main_content',
            position=3,
            content_type=ContentType.objects.get_for_model(self.html2_block),
            object_id=self.html2_block.id
        )
        self.html2_block.content_block = self.html2_content_block
        self.html2_block.save()

        self.html3_block = HTML.objects.create(content='<p>HTML Block</p>')
        self.html3_content_block = ContentBlock.objects.create(
            obj_version=self.page_version,
            column='side',
            position=4,
            content_type=ContentType.objects.get_for_model(self.html3_block),
            object_id=self.html3_block.id
        )
        self.html3_block.content_block = self.html3_content_block
        self.html3_block.save()

    def change_page_version(self):
        self.page_version.version_number = 1
        self.page_version.save()


class TestPageChangeTemplateView(BaseViewsCase):
    def setUp(self):
        super(TestPageChangeTemplateView, self).setUp()
        self.change_template_url = reverse(
            'admin:%s_%s_changetemplate' % self.info, args=(self.page_version.id,)
        )

    def test_permissions(self):
        # Permission denied as user doesn't have permissions
        response = self.editor_no_permissions_client.get(self.change_template_url)
        self.assertEqual(response.status_code, 403)

        # Editor with permissions
        response = self.editor_client.get(self.change_template_url)
        self.assertEqual(response.status_code, 302)

    def test_post(self):
        # Check POST
        response = self.editor_client.post(self.change_template_url, {
            'template_name': 'glitter/sample2.html',
        })
        self.assertEqual(response.status_code, 302)

        # Check template gets changed
        page_version = Version.objects.get(id=self.page_version.id)
        self.assertEqual(page_version.template_name, 'glitter/sample2.html')

        # These blocks get moved to a new column
        html1_content_block = ContentBlock.objects.get(id=self.html1_content_block.id)
        html2_content_block = ContentBlock.objects.get(id=self.html2_content_block.id)

        self.assertEqual(html1_content_block.column, 'content')
        self.assertEqual(html2_content_block.column, 'content')
        self.assertEqual(html1_content_block.position, 1)
        self.assertEqual(html2_content_block.position, 2)

        # Index error if ContentBlock doesn't exist
        self.editor_client.post(self.change_template_url, {
            'template_name': 'glitter/sample.html',
        })

    def test_page_owner(self):
        """ Check page owner. """
        self.page_version.owner = self.super_user
        self.page_version.save()
        response = self.editor_client.get(self.change_template_url)
        self.assertEqual(response.status_code, 403)

    def test_page_version(self):
        """ Check page version. """
        self.change_page_version()
        self.editor.user_permissions.add(self.edit_permissions)
        response = self.editor_client.get(self.change_template_url)
        self.assertEqual(response.status_code, 403)


class TestPageBlockAddView(BaseViewsCase):
    def setUp(self):
        super(TestPageBlockAddView, self).setUp()
        self.page_block_add_view_url = '{}?column=main_content'.format(reverse(
            'block_admin:%s_%s_add' % (HTML._meta.app_label, HTML._meta.model_name),
            kwargs={
                'version_id': self.page_version.id,
            }
        ))

    def test_permissions(self):
        # Permission denied as user doesn't have permissions
        response = self.editor_no_permissions_client.get(self.page_block_add_view_url)
        self.assertEqual(response.status_code, 403)

        # Editor with permissions
        response = self.editor_client.get(self.page_block_add_view_url)
        self.assertEqual(response.status_code, 200)

    def test_add_block(self):
        response = self.editor_client.post(self.page_block_add_view_url, {
            'content': '<p>Test</p>',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/glitter/update_column.html')

    def test_add_block_top(self):
        response = self.editor_client.post(self.page_block_add_view_url + '&top=true', {
            'content': '<p>Test</p>',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/glitter/update_column.html')

    def test_add_continue(self):
        response = self.editor_client.post(self.page_block_add_view_url, {
            'content': '<p>Test</p>',
            '_continue': '',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blockadmin/continue.html')

    def test_page_version(self):
        """ Check page version. """
        self.change_page_version()
        self.editor.user_permissions.add(self.edit_permissions)
        response = self.editor_client.get(self.page_block_add_view_url)
        self.assertEqual(response.status_code, 403)


class TestPageBlockDeleteView(BaseViewsCase):

    def setUp(self):
        super(TestPageBlockDeleteView, self).setUp()
        self.page_block_delete_view_url = reverse(
            'admin:%s_%s_block_delete' % self.info, args=(self.html1_content_block.id,)
        )

    def test_permissions(self):
        """ Test permissions. """
        response = self.editor_no_permissions_client.get(self.page_block_delete_view_url)
        self.assertEqual(response.status_code, 403)

        # Editor with permissions
        response = self.editor_client.get(self.page_block_delete_view_url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):

        response = self.editor_client.post(self.page_block_delete_view_url, {
            'column': 'main_content',
            'block_type': u'glitter_html_block.HTML',
        })
        self.assertEqual(response.status_code, 200)

    def test_page_version(self):
        """ Check page version. """
        self.change_page_version()
        self.editor.user_permissions.add(self.edit_permissions)
        response = self.editor_client.get(self.page_block_delete_view_url)
        self.assertEqual(response.status_code, 403)


class TestPageBlockMoveView(BaseViewsCase):
    def setUp(self):
        super(TestPageBlockMoveView, self).setUp()
        self.html1_block_move_view_url = reverse(
            'admin:%s_%s_block_move' % self.info, args=(self.html1_content_block.id,)
        )
        self.html2_block_move_view_url = reverse(
            'admin:%s_%s_block_move' % self.info, args=(self.html2_content_block.id,)
        )
        self.html3_block_move_view_url = reverse(
            'admin:%s_%s_block_move' % self.info, args=(self.html3_content_block.id,)
        )

    def test_permissions(self):
        """ Test permissions. """
        response = self.editor_no_permissions_client.get(self.html1_block_move_view_url)
        self.assertEqual(response.status_code, 403)

        # Editor with permissions
        response = self.editor_client.get(self.html1_block_move_view_url)
        self.assertEqual(response.status_code, 200)

    def test_html1_move_block_bottom(self):
        """ Move block top. """
        response = self.editor_client.post(self.html1_block_move_view_url, {
            'move': MoveBlockForm.MOVE_BOTTOM,
        })
        self.assertEqual(response.status_code, 200)

    def test_html2_move_block_bottom(self):
        """ Move block up. """
        response = self.editor_client.post(self.html2_block_move_view_url, {
            'move': MoveBlockForm.MOVE_BOTTOM,
        })
        self.assertEqual(response.status_code, 200)

    def test_html3_move_block_bottom(self):
        """ Move block down. """
        response = self.editor_client.post(self.html3_block_move_view_url, {
            'move': MoveBlockForm.MOVE_BOTTOM
        })
        self.assertEqual(response.status_code, 200)

    def test_move_html1_block_top(self):
        # Move block bottom
        response = self.editor_client.post(self.html1_block_move_view_url, {
            'move': MoveBlockForm.MOVE_TOP
        })
        self.assertEqual(response.status_code, 200)

    def test_move_html2_block_top(self):
        # Move block bottom
        response = self.editor_client.post(self.html2_block_move_view_url, {
            'move': MoveBlockForm.MOVE_TOP
        })
        self.assertEqual(response.status_code, 200)

    def test_move_html1_block_up(self):
        # Move block bottom
        response = self.editor_client.post(self.html1_block_move_view_url, {
            'move': MoveBlockForm.MOVE_UP
        })
        self.assertEqual(response.status_code, 200)

    def test_move_html1_block_down(self):
        # Move block bottom
        response = self.editor_client.post(self.html1_block_move_view_url, {
            'move': MoveBlockForm.MOVE_DOWN
        })
        self.assertEqual(response.status_code, 200)

    def test_page_version(self):
        """ Check page version. """
        self.change_page_version()
        self.editor.user_permissions.add(self.edit_permissions)
        response = self.editor_client.get(self.html1_block_move_view_url)
        self.assertEqual(response.status_code, 403)


class TestPageBlockColumnView(BaseViewsCase):

    def setUp(self):
        super(TestPageBlockColumnView, self).setUp()
        self.html1_block_column_url = reverse(
            'admin:%s_%s_block_column' % self.info, args=(self.html1_content_block.id,)
        )

    def test_permissions(self):
        """ Test permissions. """
        response = self.editor_no_permissions_client.get(self.html1_block_column_url)
        self.assertEqual(response.status_code, 403)

        # Editor with permissions
        response = self.editor_client.get(self.html1_block_column_url)
        self.assertEqual(response.status_code, 200)

    def test_move_block_side(self):
        """ Move block side. """
        response = self.editor_client.post(self.html1_block_column_url, {
            'move': 'side',
        })
        self.assertEqual(response.status_code, 200)

    def test_get_last_block(self):
        self.html3_block.delete()
        self.html3_content_block.delete()

        response = self.editor_client.post(self.html1_block_column_url, {
            'move': 'side',
        })
        self.assertEqual(response.status_code, 200)

    def test_page_version(self):
        """ Check page version. """
        self.change_page_version()
        self.editor.user_permissions.add(self.edit_permissions)
        response = self.editor_client.get(self.html1_block_column_url)
        self.assertEqual(response.status_code, 403)
