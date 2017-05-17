from __future__ import unicode_literals

from django.test import TestCase

from .factories import PageFactory, PageVersionFactory


class TestGlitterMixinPublished(TestCase):
    def test_published_true(self):
        page = PageFactory()

        self.assertFalse(page.is_published)

    def test_all_false(self):
        page = PageFactory(published=False)

        self.assertFalse(page.is_published)

    def test_unpublished(self):
        page_version = PageVersionFactory()
        page = page_version.content_object

        self.assertFalse(page.is_published)

    def test_all_true(self):
        page_version = PageVersionFactory(version_number=1, set_version=True)
        page = page_version.content_object

        self.assertTrue(page.is_published)
