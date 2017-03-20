from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from glitter.models import Version
from glitter.pages.models import Page
from glitter.publisher.models import PublishAction


class TestPublishAction(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='admin',
        )
        cls.page = Page.objects.create(
            url='/test/',
            title='Test',
        )
        cls.page_content_type = ContentType.objects.get_for_model(cls.page)

        cls.version_1 = Version.objects.create(
            content_type=cls.page_content_type,
            object_id=cls.page.pk,
            template_name='demo.html',
            version_number=1,
        )
        cls.version_2 = Version.objects.create(
            content_type=cls.page_content_type,
            object_id=cls.page.pk,
            template_name='demo.html',
            version_number=2,
        )

    def setUp(self):
        self.page.refresh_from_db()

    def test_publish(self):
        obj = PublishAction(
            content_type=self.page_content_type,
            object_id=self.page.pk,
            publish_version=1,
            user=self.user,
        )

        actioned = obj.process_action()

        self.page.refresh_from_db()
        self.assertTrue(actioned)
        self.assertEqual(self.page.current_version, self.version_1)

    def test_publish_no_action(self):
        self.page.current_version = self.version_1
        self.page.save()
        obj = PublishAction(
            content_type=self.page_content_type,
            object_id=self.page.pk,
            publish_version=1,
            user=self.user,
        )

        actioned = obj.process_action()

        self.page.refresh_from_db()
        self.assertEqual(self.page.current_version, self.version_1)
        self.assertFalse(actioned)

    def test_unpublish(self):
        self.page.current_version = self.version_1
        self.page.save()
        obj = PublishAction(
            content_type=self.page_content_type,
            object_id=self.page.pk,
            publish_version=PublishAction.UNPUBLISH_CHOICE,
            user=self.user,
        )

        actioned = obj.process_action()

        self.page.refresh_from_db()
        self.assertTrue(actioned)
        self.assertIsNone(self.page.current_version)

    def test_unpublish_no_action(self):
        obj = PublishAction(
            content_type=self.page_content_type,
            object_id=self.page.pk,
            publish_version=PublishAction.UNPUBLISH_CHOICE,
            user=self.user,
        )

        actioned = obj.process_action()

        self.page.refresh_from_db()
        self.assertFalse(actioned)
        self.assertIsNone(self.page.current_version)
