# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from glitter.models import Version, ContentBlock
from glitter.pages.models import Page
from glitter.pages.validators import validate_page_url
from glitter.blocks.html.models import HTML

from .factories import PageFactory, PageVersionFactory


class TestModelsPage(TestCase):
    def setUp(self):
        # Page
        self.page = Page.objects.create(url='/test/', title='Test page')

        page_content_type = ContentType.objects.get_for_model(Page)

        # Page version.
        self.page_version = Version.objects.create(
            content_type=page_content_type,
            object_id=self.page.id,
            template_name='glitter/sample.html',
        )

        self.html1_block = HTML.objects.create(content='<p>HTML Block</p>')
        self.html1_content_block = ContentBlock.objects.create(
            obj_version=self.page_version,
            column='Main Content',
            position=1,
            content_type=ContentType.objects.get_for_model(self.html1_block),
            object_id=self.html1_block.id
        )
        self.html1_block.content_block = self.html1_content_block
        self.html1_block.save()

        self.html2_block = HTML.objects.create(content='<p>HTML Block</p>')
        self.html2_content_block = ContentBlock.objects.create(
            obj_version=self.page_version,
            column='Main Content',
            position=2,
            content_type=ContentType.objects.get_for_model(self.html2_block),
            object_id=self.html2_block.id
        )
        self.html2_block.content_block = self.html2_content_block
        self.html2_block.save()

        self.html3_block = HTML.objects.create(content='<p>HTML Block</p>')
        self.html3_content_block = ContentBlock.objects.create(
            obj_version=self.page_version,
            column='Main Content',
            position=3,
            content_type=ContentType.objects.get_for_model(self.html3_block),
            object_id=self.html3_block.id
        )
        self.html3_block.content_block = self.html3_content_block
        self.html3_block.save()

    def test_validate_page_url(self):
        self.assertRaises(ValidationError, validate_page_url, value='admin')
        self.assertRaises(ValidationError, validate_page_url, value='/admin')
        self.assertRaises(ValidationError, validate_page_url, value='//')

    def test_manager_published(self):
        self.page_version.generate_version()
        self.page_version.save()

        self.page.published = True
        self.page.current_version = self.page_version
        self.page.save()

        self.assertEqual(1, Page.objects.published().count())

    def test_page_version_str(self):
        self.page_version.__str__()

        # Test __str__ by adding version number.
        self.page_version.version_number = 1
        self.page_version.save()
        self.page_version.__str__()

    def test_generate_version(self):
        self.page_version.generate_version()

        # Test removing version number
        self.page_version.version_number = 1
        self.page_version.save()
        self.page_version.generate_version()

    def test_is_published(self):
        self.page_version.is_published

        # Test removing version number
        self.page_version.version_number = 1
        self.page_version.save()
        self.page.current_version = self.page_version

        self.page_version.is_published

    def test_content_block_last_position(self):
        """Test if position is added if last_position is None."""

        ContentBlock.objects.update(position=None)

        self.html1_content_block.position = None
        self.html1_content_block.save()
        self.assertEqual(self.html1_content_block.position, 1)

        self.html2_content_block.position = None
        self.html2_content_block.save()
        self.assertEqual(self.html1_content_block.position, 1)


class TestPageIsVisible(TestCase):
    def test_not_in_navigation(self):
        page = PageFactory(show_in_navigation=False)

        self.assertFalse(page.is_visible)

    def test_unpublished_page(self):
        page_version = PageVersionFactory()
        page = page_version.content_object

        self.assertFalse(page.is_visible)

    def test_published_page(self):
        page_version = PageVersionFactory(version_number=1, set_version=True)
        page = page_version.content_object

        self.assertTrue(page.is_visible)

    def test_page_with_app(self):
        page = PageFactory(glitter_app_name='fake')

        self.assertTrue(page.is_visible)
