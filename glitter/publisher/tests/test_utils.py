from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import SimpleTestCase, TestCase, override_settings
from django.utils import timezone

from glitter.models import Version
from glitter.pages.models import Page
from glitter.publisher.models import PublishAction
from glitter.publisher.utils import process_actions, celery_enabled


@override_settings(GLITTER_PUBLISHER_CELERY=False)
class TestProcessActions(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='admin',
        )
        page = Page.objects.create(
            url='/test/',
            title='Test',
        )
        page_content_type = ContentType.objects.get_for_model(page)

        Version.objects.create(
            content_type=page_content_type,
            object_id=page.pk,
            template_name='demo.html',
            version_number=1,
        )

        cls.action_1 = PublishAction.objects.create(
            content_type=page_content_type,
            object_id=page.pk,
            scheduled_time=timezone.now(),
            publish_version=1,
            user=user,
        )

        cls.action_2 = PublishAction.objects.create(
            content_type=page_content_type,
            object_id=page.pk,
            scheduled_time=timezone.now(),
            publish_version=1,
            user=user,
        )

    def test_all_actions(self):
        actions = process_actions()

        self.assertEqual(actions, 2)
        self.assertEqual(PublishAction.objects.count(), 0)

    def test_one_action(self):
        actions = process_actions(action_ids=[self.action_1.id])

        self.assertEqual(actions, 1)
        self.assertEqual(PublishAction.objects.count(), 1)


class TestCeleryEnabled(SimpleTestCase):
    @override_settings(GLITTER_PUBLISHER_CELERY=True)
    def test_celery_enabled(self):
        enabled = celery_enabled()

        self.assertTrue(enabled)

    @override_settings(GLITTER_PUBLISHER_CELERY=False)
    def test_celery_disabled(self):
        enabled = celery_enabled()

        self.assertFalse(enabled)
