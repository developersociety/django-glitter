from datetime import timedelta
try:
    from unittest import mock
except ImportError:
    import mock

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import management
from django.test import TestCase, override_settings
from django.utils import six, timezone

from glitter.models import Version
from glitter.pages.models import Page
from glitter.reminders import choices
from glitter.reminders.models import Reminder


@override_settings(
    ROOT_URLCONF='glitter.reminders.tests.urls',
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

    def create_page_with_version(self, modified):
        self.page = Page.objects.create(url='/test/', title='Test page')
        with mock.patch('django.db.models.fields.DateTimeField.pre_save') as mock_pre_save:
            mock_pre_save.return_value = modified
            self.page_version = Version.objects.create(
                content_type=ContentType.objects.get_for_model(Page),
                object_id=self.page.id,
                template_name='glitter/sample.html',
                owner=self.user
            )
            self.page_version.generate_version()
            self.page.current_version = self.page_version
            self.page.current_version.modified = mock.Mock(
                return_value=timezone.now() - timedelta(days=16)
            )
            self.page.save()

    def create_reminder(self, interval, page):
        self.reminder = Reminder.objects.create(
            interval=interval,
            content_type=ContentType.objects.get_for_model(Page),
            object_id=self.page.id,
            user=self.user
        )

    def test_send_reminder(self):
        """ Send reminder in two weeks interal. """
        # More then two weeks ago.
        modified_at = timezone.now() - timedelta(days=16)

        self.create_page_with_version(modified=modified_at)
        self.create_reminder(
            interval=choices.INTERVAL_2_WEEKS, page=self.page
        )
        self.reminder.sent_at = modified_at
        self.reminder.save()

        management.call_command('send_reminders', stdout=self.stdout, verbosity=3)
        command_output = self.stdout.getvalue().strip()

        self.assertEqual(
            command_output,
            'Email for {} is sent to: {}'.format(
                self.reminder.content_object, self.reminder.user.email
            )
        )

    def test_not_send_reminder_next_day(self):
        """
        Should not sent reminder if content updated 16 days ago but reminder was sent 1 day ago
        based on 2 weeks interval.
        """
        modified_at = timezone.now() - timedelta(days=16)

        self.create_page_with_version(modified=modified_at)
        self.create_reminder(
            choices.INTERVAL_2_WEEKS, self.page
        )
        self.reminder.sent_at = timezone.now() - timedelta(days=1)
        self.reminder.save()

        self.stdout = six.StringIO()

        management.call_command('send_reminders', stdout=self.stdout, verbosity=3)

        command_output = self.stdout.getvalue().strip()
        self.assertEqual(
            command_output,
            'Email for {} is not sent to: {}'.format(
                self.reminder.content_object, self.reminder.user.email
            )
        )

    def test_reminder_sent_at(self):
        """
        Test if sent_at set 100 days ago and the content was modified 3 days ago based on 2 weeks
        interval.
        """
        modified_at = timezone.now() - timedelta(days=3)

        self.create_page_with_version(modified=modified_at)
        self.create_reminder(choices.INTERVAL_2_WEEKS, self.page)

        self.reminder.sent_at = timezone.now() - timedelta(days=100)
        self.reminder.save()

        self.stdout = six.StringIO()
        management.call_command('send_reminders', stdout=self.stdout, verbosity=3)
        command_output = self.stdout.getvalue().strip()
        self.assertEqual(
            command_output,
            'Email for {} is not sent to: {}'.format(
                self.reminder.content_object, self.reminder.user.email
            )
        )
