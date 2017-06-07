# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
from unittest import skipIf

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import override_settings, modify_settings, TestCase
from django.test.client import Client

from glitter.blocks.html.models import HTML
from glitter.pages.models import Page
from glitter.models import Version, ContentBlock


SAMPLE_BLOCK_MISSING = 'glitter.tests.sampleblocks' not in settings.INSTALLED_APPS
if not SAMPLE_BLOCK_MISSING:
    from glitter.tests.sampleblocks.models import (
        SampleModel, SampleModelWithInlinesBlock, SampleInline
    )


@modify_settings(INSTALLED_APPS={
    'append': 'glitter.tests.sampleblocks',
    'append': 'glitter.tests.sample',
})
@override_settings(
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'glitter.pages.middleware.PageFallbackMiddleware',
    ),
    TEMPLATE_DIRS=(
        os.path.join(os.path.dirname(__file__), 'templates'),
    ),
)
class BaseEditCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseEditCase, cls).setUpClass()

        # Permissions
        edit_perm = Permission.objects.get_by_natural_key('edit_page', 'glitter_pages', 'page')
        publish_perm = Permission.objects.get_by_natural_key(
            'publish_page', 'glitter_pages', 'page'
        )

        # Content type used regularly
        cls.page_content_type = ContentType.objects.get_for_model(Page)

        # Staff - admin access without pages permissions
        cls.staff = User.objects.create_user(username='staff', password='staff')
        cls.staff.is_staff = True
        cls.staff.save()
        cls.staff_client = Client()
        cls.staff_client.login(username='staff', password='staff')

        # Editor - can edit pages but can't publish
        cls.editor = User.objects.create_user(username='editor', password='editor')
        cls.editor.is_staff = True
        cls.editor.save()
        cls.editor.user_permissions.add(edit_perm)
        cls.editor_client = Client()
        cls.editor_client.login(username='editor', password='editor')

        # Other editor, testing cases which protect users content
        cls.editor2 = User.objects.create_user(username='editor2', password='editor2')
        cls.editor2.is_staff = True
        cls.editor2.save()
        cls.editor2.user_permissions.add(edit_perm)
        cls.editor2_client = Client()
        cls.editor2_client.login(username='editor2', password='editor2')

        # Publisher - can edit and publish pages
        cls.publisher = User.objects.create_user(username='publisher', password='publisher')
        cls.publisher.is_staff = True
        cls.publisher.save()
        cls.publisher.user_permissions.add(edit_perm, publish_perm)
        cls.publisher_client = Client()
        cls.publisher_client.login(username='publisher', password='publisher')

        # Other publisher
        cls.publisher2 = User.objects.create_user(username='publisher2', password='publisher2')
        cls.publisher2.is_staff = True
        cls.publisher2.save()
        cls.publisher2.user_permissions.add(edit_perm, publish_perm)
        cls.publisher2_client = Client()
        cls.publisher2_client.login(username='publisher2', password='publisher2')

        # Anonymous user
        cls.anon_client = Client()


class TestNoSavedVersions(BaseEditCase):
    def setUp(self):
        super(TestNoSavedVersions, self).setUp()

        # Simple page without any saved versions
        self.page_url = '/no-saved-versions/'
        Page.objects.create(url=self.page_url, title='Test page')

    def test_anon_user(self):
        # 404 for non-editors
        response = self.anon_client.get(self.page_url)
        self.assertEqual(response.status_code, 404)

    def test_editor(self):
        # 200 with link for editors
        response = self.editor_client.get(self.page_url)
        self.assertEqual(response.status_code, 200)


class TestCreateVersion(BaseEditCase):
    def setUp(self):
        super(TestCreateVersion, self).setUp()

        # Simple page without any saved versions
        page = Page.objects.create(url='/create-version/', title='Test page')

        # Change template URL
        info = page._meta.app_label, page._meta.model_name
        self.change_template_url = reverse('admin:%s_%s_template' % info, kwargs={
            'object_id': page.id,
        })

    def test_anon_user(self):
        # No for anon users
        response = self.anon_client.get(self.change_template_url, follow=True)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_staff(self):
        # No for staff
        response = self.staff_client.get(self.change_template_url)
        self.assertEqual(response.status_code, 403)

    def test_editor(self):
        # Editor can create a new version
        response = self.editor_client.get(self.change_template_url)
        self.assertTemplateUsed(response, 'admin/glitter/new_template.html')

        response = self.editor_client.post(self.change_template_url, {
            'template_name': 'glitter/sample.html',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'glitter/sample.html')


class TestViewVersion(BaseEditCase):
    def setUp(self):
        super(TestViewVersion, self).setUp()

        # Page with one unsaved version
        page = Page.objects.create(url='/view-version/', title='Test page')
        page_version = Version.objects.create(
            content_type=self.page_content_type, object_id=page.id,
            template_name='glitter/sample.html', owner=self.editor)

        # View page version URL
        info = page._meta.app_label, page._meta.model_name
        self.view_version_url = reverse('admin:%s_%s_version' % info, kwargs={
            'version_id': page_version.id,
        })

    def test_anon_user(self):
        # No for anon users
        response = self.anon_client.get(self.view_version_url, follow=True)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_staff(self):
        # No for staff
        response = self.staff_client.get(self.view_version_url)
        self.assertEqual(response.status_code, 403)

    def test_other_editor(self):
        # No for other editor
        response = self.editor2_client.get(self.view_version_url)
        self.assertEqual(response.status_code, 403)

    def test_editor(self):
        # Editor can view their own version
        response = self.editor_client.get(self.view_version_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')


class TestRedirectVersion(BaseEditCase):
    def setUp(self):
        super(TestRedirectVersion, self).setUp()

        # Page with two unsaved versions
        self.page_url = '/redirect-version/'
        self.page = Page.objects.create(url=self.page_url, title='Test page')
        self.page_version_1 = Version.objects.create(
            content_type=self.page_content_type, object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor)
        self.page_version_2 = Version.objects.create(
            content_type=self.page_content_type, object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor2)

        # Redirect page URL
        info = self.page._meta.app_label, self.page._meta.model_name
        self.redirect_url = reverse('admin:%s_%s_redirect' % info, kwargs={
            'object_id': self.page.id,
        })

        # Editors URLs
        self.view_version_1_url = reverse('admin:%s_%s_version' % info, kwargs={
            'version_id': self.page_version_1.id,
        })
        self.view_version_2_url = reverse('admin:%s_%s_version' % info, kwargs={
            'version_id': self.page_version_2.id,
        })

        # New template URL
        self.new_template_url = reverse('admin:%s_%s_template' % info, kwargs={
            'object_id': self.page.id,
        })

    def test_anon_user(self):
        # No for anon users
        response = self.anon_client.get(self.redirect_url, follow=True)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_staff(self):
        # No for staff
        response = self.staff_client.get(self.redirect_url)
        self.assertEqual(response.status_code, 403)

    def test_other_editor(self):
        # Other editor gets asked to start with a new template (we're using the publisher though)
        response = self.publisher_client.get(self.redirect_url, follow=True)
        self.assertRedirects(response, self.new_template_url)
        self.assertTemplateUsed(response, 'admin/glitter/new_template.html')

    def test_editors(self):
        # Each editor gets redirected to their latest version
        response = self.editor_client.get(self.redirect_url)
        self.assertRedirects(response, self.view_version_1_url)

        response = self.editor2_client.get(self.redirect_url)
        self.assertRedirects(response, self.view_version_2_url)

    def test_published_page(self):
        # With a published page, editors always get redirected to it
        self.page_version_1.generate_version()
        self.page_version_1.save()
        self.page.current_version = self.page_version_1
        self.page.save()

        response = self.editor_client.get(self.redirect_url)
        self.assertRedirects(response, self.page_url)

        response = self.editor2_client.get(self.redirect_url)
        self.assertRedirects(response, self.page_url)


class TestEditVersion(BaseEditCase):
    def setUp(self):
        super(TestEditVersion, self).setUp()

        # Page with one unsaved version
        page = Page.objects.create(url='/edit-version/', title='Test page')
        self.page_version = Version.objects.create(
            content_type=self.page_content_type, object_id=page.id,
            template_name='glitter/sample.html', owner=self.editor)

        # View page version URL
        info = page._meta.app_label, page._meta.model_name
        self.edit_version_url = reverse('admin:%s_%s_edit' % info, kwargs={
            'version_id': self.page_version.id,
        })
        self.view_version_url = reverse('admin:%s_%s_version' % info, kwargs={
            'version_id': self.page_version.id,
        })

    def test_anon_user(self):
        # No for anon users
        response = self.anon_client.get(self.edit_version_url, follow=True)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_staff(self):
        # No for staff
        response = self.staff_client.get(self.edit_version_url)
        self.assertEqual(response.status_code, 403)

    def test_other_editor(self):
        # No for other editor
        response = self.editor2_client.get(self.edit_version_url)
        self.assertEqual(response.status_code, 403)

    def test_editor_unsaved_post(self):
        # Unsaved POST will redirect to the same URL
        response = self.editor_client.post(self.edit_version_url, {
            'template_name': 'glitter/sample.html',
        }, follow=True)
        self.assertRedirects(response, self.edit_version_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')

    def test_editor_saved_get(self):
        # Save the version
        self.page_version.generate_version()
        self.page_version.save()

        # Get will redirect to the view URL
        response = self.editor_client.get(self.edit_version_url, follow=True)
        self.assertRedirects(response, self.view_version_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')


@skipIf(SAMPLE_BLOCK_MISSING, 'glitter.tests.sampleblocks is not installed')
class TestEditCopyVersion(BaseEditCase):
    def setUp(self):
        super(TestEditCopyVersion, self).setUp()

        # Page with one saved version, an HTML block, and sample blocks
        page = Page.objects.create(url='/edit-version/', title='Test page')
        page_version = Version.objects.create(
            content_type=self.page_content_type, object_id=page.id,
            template_name='glitter/sample.html', owner=self.editor)

        html_block = HTML.objects.create(content='<p>HTML Block</p>')
        content_block = ContentBlock.objects.create(
            obj_version=page_version, column='content', position=1,
            content_type=ContentType.objects.get_for_model(html_block), object_id=html_block.id)
        html_block.content_block = content_block
        html_block.save()

        sample_model = SampleModel.objects.create(content='<p>Sample Model</p>')
        sample_block = SampleModelWithInlinesBlock.objects.create()
        SampleInline.objects.create(parent_block=sample_block, foreign_model=sample_model)
        content_block = ContentBlock.objects.create(
            obj_version=page_version, column='content', position=2,
            content_type=ContentType.objects.get_for_model(sample_block), object_id=sample_block.id
        )
        sample_block.content_block = content_block
        sample_block.save()

        page_version.generate_version()
        page_version.save()

        # Edit page URLs
        info = page._meta.app_label, page._meta.model_name
        self.edit_version1_url = reverse('admin:%s_%s_edit' % info, kwargs={
            'version_id': page_version.id,
        })
        self.edit_version2_url = reverse('admin:%s_%s_edit' % info, kwargs={
            'version_id': page_version.id + 1,
        })

    def test_edit_copy_version(self):
        # Generate a new page version
        response = self.editor_client.post(self.edit_version1_url, follow=True)
        self.assertRedirects(response, self.edit_version2_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')


class TestSaveVersion(BaseEditCase):
    def setUp(self):
        super(TestSaveVersion, self).setUp()

        # Page with one unsaved version
        page = Page.objects.create(url='/save-version/', title='Test page')
        self.page_version = Version.objects.create(
            content_type=self.page_content_type, object_id=page.id,
            template_name='glitter/sample.html', owner=self.editor)

        # View page version URL
        info = page._meta.app_label, page._meta.model_name
        self.save_version_url = reverse('admin:%s_%s_save' % info, kwargs={
            'version_id': self.page_version.id,
        })
        self.view_version_url = reverse('admin:%s_%s_version' % info, kwargs={
            'version_id': self.page_version.id,
        })

    def test_anon_user(self):
        # No for anon users
        response = self.anon_client.post(self.save_version_url, follow=True)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_editor_get(self):
        # Have to POST to save
        response = self.editor_client.get(self.save_version_url)
        self.assertEqual(response.status_code, 405)

    def test_staff(self):
        # No for staff
        response = self.staff_client.post(self.save_version_url)
        self.assertEqual(response.status_code, 403)

    def test_other_editor(self):
        # No for other editor
        response = self.editor2_client.post(self.save_version_url)
        self.assertEqual(response.status_code, 403)

    def test_editor(self):
        # Generates a version number
        response = self.editor_client.post(self.save_version_url, follow=True)
        page_version = Version.objects.get(id=self.page_version.id)  # refetch
        self.assertNotEqual(page_version.version_number, None)
        self.assertRedirects(response, self.view_version_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')

    def test_editor_saved_version(self):
        # Generate a saved version
        self.page_version.generate_version()
        self.page_version.save()

        # User will just be redirected to the version view page
        response = self.editor_client.post(self.save_version_url, follow=True)
        page_version = Version.objects.get(id=self.page_version.id)  # refetch
        self.assertEqual(self.page_version.version_number, page_version.version_number)
        self.assertRedirects(response, self.view_version_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')


class TestPublishVersion(BaseEditCase):
    def setUp(self):
        super(TestPublishVersion, self).setUp()

        # Page with one unsaved version
        self.page_url = '/publish-version/'
        self.page = Page.objects.create(url=self.page_url, title='Test page')
        self.page_version = Version.objects.create(
            content_type=self.page_content_type, object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor)

        # Edit page URLs
        info = self.page._meta.app_label, self.page._meta.model_name
        self.publish_version_url = reverse('admin:%s_%s_publish' % info, kwargs={
            'version_id': self.page_version.id,
        })

    def test_anon_user(self):
        # No for anon users
        response = self.anon_client.post(self.publish_version_url, follow=True)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_publisher_post(self):
        # Have to POST to publish
        response = self.editor_client.get(self.publish_version_url)
        self.assertEqual(response.status_code, 405)

    def test_staff(self):
        # No for staff
        response = self.staff_client.post(self.publish_version_url)
        self.assertEqual(response.status_code, 403)

    def test_other_publisher(self):
        # No for other publisher
        response = self.publisher2_client.post(self.publish_version_url)
        self.assertEqual(response.status_code, 403)

    def test_editor(self):
        # Editor without publish permission can't publish
        response = self.editor_client.post(self.publish_version_url)
        self.assertEqual(response.status_code, 403)

    def test_publish_unsaved(self):
        # Change the object owner for testing
        self.page_version.owner = self.publisher
        self.page_version.save()

        # Unsaved version publish saves a new version number, and redirects to the live URL
        response = self.publisher_client.post(self.publish_version_url, follow=True)
        page_version = Version.objects.get(id=self.page_version.id)  # refetch
        self.assertNotEqual(page_version.version_number, None)
        self.assertRedirects(response, self.page.get_absolute_url())
        self.assertTemplateUsed(response, 'glitter/sample.html')

    def test_publish_saved(self):
        self.page_version.owner = self.publisher
        self.page_version.generate_version()
        self.page_version.save()

        # Unsaved version publish saves a new version number, and redirects to the live URL
        response = self.publisher_client.post(self.publish_version_url, follow=True)
        self.assertRedirects(response, self.page.get_absolute_url())
        self.assertTemplateUsed(response, 'glitter/sample.html')

    def test_publish_current_version(self):
        self.page_version.owner = self.publisher
        self.page_version.generate_version()
        self.page_version.save()
        self.page.current_version = self.page_version
        self.page.save()

        # This should just redirect to the live URL
        response = self.publisher_client.post(self.publish_version_url, follow=True)
        page_version = Version.objects.get(id=self.page_version.id)  # refetch
        self.assertEqual(self.page_version.version_number, page_version.version_number)
        self.assertRedirects(response, self.page_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')


class TestUnpublishVersion(BaseEditCase):
    def setUp(self):
        super(TestUnpublishVersion, self).setUp()

        # Page with one published version
        self.page_url = '/edit-version/'
        self.page = Page.objects.create(url=self.page_url, title='Test page')
        self.page_version = Version(
            content_type=self.page_content_type, object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor)
        self.page_version.generate_version()
        self.page_version.save()
        self.page.current_version = self.page_version
        self.page.save()

        # Edit page URLs
        info = self.page._meta.app_label, self.page._meta.model_name
        self.unpublish_version_url = reverse('admin:%s_%s_unpublish' % info, kwargs={
            'version_id': self.page_version.id,
        })
        self.view_version_url = reverse('admin:%s_%s_version' % info, kwargs={
            'version_id': self.page_version.id,
        })

    def test_anon_user(self):
        # No for anon users
        response = self.anon_client.post(self.unpublish_version_url, follow=True)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_publisher_post(self):
        # Have to POST to unpublish
        response = self.editor_client.get(self.unpublish_version_url)
        self.assertEqual(response.status_code, 405)

    def test_staff(self):
        # No for staff
        response = self.staff_client.post(self.unpublish_version_url)
        self.assertEqual(response.status_code, 403)

    def test_editor(self):
        # Editor without publish permission can't unpublish
        response = self.editor_client.post(self.unpublish_version_url)
        self.assertEqual(response.status_code, 403)

    def test_unpublish(self):
        # We'll be redirected to the view version which is just unpublished
        response = self.publisher_client.post(self.unpublish_version_url, follow=True)
        page = Page.objects.get(id=self.page.id)  # refetch
        self.assertEqual(page.current_version, None)
        self.assertRedirects(response, self.view_version_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')

    def test_unpublish_not_current(self):
        new_version = Version(
            content_type=self.page_content_type, object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor)
        new_version.generate_version()
        new_version.save()
        self.page.current_version = new_version
        self.page.save()

        # Unsaved version publish saves a new version number, and redirects to the live URL
        response = self.publisher_client.post(self.unpublish_version_url, follow=True)
        page = Page.objects.get(id=self.page.id)  # refetch
        self.assertEqual(page.current_version.id, new_version.id)
        self.assertRedirects(response, self.view_version_url)
        self.assertTemplateUsed(response, 'glitter/sample.html')


class TestDiscardVersion(BaseEditCase):
    def setUp(self):
        super(TestDiscardVersion, self).setUp()

        # Page with one saved version, one unsaved version
        self.page_url = '/edit-version/'
        self.page = Page.objects.create(url=self.page_url, title='Test page')
        self.page_version_1 = Version(
            content_type=self.page_content_type, object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor)
        self.page_version_1.generate_version()
        self.page_version_1.save()
        self.page.current_version = self.page_version_1
        self.page.save()
        self.page_version_2 = Version.objects.create(
            content_type=self.page_content_type, object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.editor)

        # Unsaved version has an HTML block
        html_block = HTML.objects.create(content='<p>HTML Block</p>')
        content_block = ContentBlock.objects.create(
            obj_version=self.page_version_2, column='main_content', position=1,
            content_type=ContentType.objects.get_for_model(html_block), object_id=html_block.id)
        html_block.content_block = content_block
        html_block.save()

        # Discard page URLs
        info = self.page._meta.app_label, self.page._meta.model_name
        self.discard_version_1_url = reverse('admin:%s_%s_discard' % info, kwargs={
            'version_id': self.page_version_1.id,
        })
        self.discard_version_2_url = reverse('admin:%s_%s_discard' % info, kwargs={
            'version_id': self.page_version_2.id,
        })

    def test_anon_user(self):
        # No for anon users
        response = self.anon_client.post(self.discard_version_2_url, follow=True)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_staff(self):
        # No for staff
        response = self.staff_client.post(self.discard_version_2_url)
        self.assertEqual(response.status_code, 403)

    def test_saved_version(self):
        # Can't discard a saved version
        response = self.editor_client.post(self.discard_version_1_url)
        self.assertEqual(response.status_code, 403)

    def test_other_editor(self):
        # No for other editor
        response = self.editor2_client.post(self.discard_version_2_url)
        self.assertEqual(response.status_code, 403)

    def test_discard_get(self):
        # Discard popup loads a simple form
        response = self.editor_client.get(self.discard_version_2_url)
        self.assertTemplateUsed(response, 'admin/glitter/version_discard.html')

    def test_discard_post(self):
        # Version gets deleted
        response = self.editor_client.post(self.discard_version_2_url)
        self.assertRaises(
            Version.DoesNotExist, Version.objects.get, id=self.page_version_2.id)
        self.assertTemplateUsed(response, 'admin/glitter/version_discarded.html')
