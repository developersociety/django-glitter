from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings
from django.utils import timezone, six

from django.core import management

from glitter.models import Version
from glitter.pages.models import Page
from glitter.reminders import choices
from glitter.reminders.models import Reminder


@override_settings(
    DEBUG=True,
    ROOT_URLCONF='glitter.reminders.tests.urls',
    DEBUG_TOOLBAR_PATCH_SETTINGS=False,
)
class ReminderManagementTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='joe', password='qwerty', email='test@gmail.com'
        )
        self.stdout = six.StringIO()
        self.stderr = six.StringIO()

    def tearDown(self):
        self.stdout.close()
        self.stderr.close()

    def create_page_with_version(self, modified_at):
        self.page = Page.objects.create(url='/test/', title='Test page')
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page), object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.user, modified=modified_at,
        )
        modified_field = self.page_version._meta.get_field('modified')
        modified_field.auto_now = False
        self.page_version.modified = modified_at
        self.page_version.save()

        self.page_version.generate_version()
        self.page.current_version = self.page_version
        self.page.save()

    def create_reminder(self, interval, page):
        self.reminder = Reminder.objects.create(
            interval=interval,
            content_type=ContentType.objects.get_for_model(Page),
            object_id=self.page.id,
            user=self.user
        )

    def test_send_reminder(self):
        modified_at = timezone.now() - timedelta(days=16)

        self.create_page_with_version(modified_at=modified_at)
        self.create_reminder(choices.INTERVAL_2_WEEKS, self.page)

        management.call_command('send_reminders', stdout=self.stdout)
        command_output = self.stdout.getvalue().strip()

        self.assertEqual(
            command_output,
            'Email for {} is sent to: {}'.format(
                self.reminder.content_object, self.reminder.user.email
            )
        )

    def test_not_send_reminder_next_day(self):
        modified_at = timezone.now() - timedelta(days=16)

        self.create_page_with_version(modified_at=modified_at)
        self.create_reminder(choices.INTERVAL_2_WEEKS, self.page)

        self.reminder.sent_at = timezone.now()
        self.reminder.save()

        self.stdout = six.StringIO()
        management.call_command('send_reminders', stdout=self.stdout)
        command_output = self.stdout.getvalue().strip()
        self.assertEqual(
            command_output,
            'Email for {} is not sent to: {}'.format(
                self.reminder.content_object, self.reminder.user.email
            )
        )
