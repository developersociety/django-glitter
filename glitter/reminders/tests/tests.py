import datetime

from django.contrib.admin.sites import AdminSite
from django.test import TestCase, override_settings

from glitter.pages.admin import PageAdmin
from glitter.pages.models import Page
from glitter.reminders.admin import ReminderInline
from glitter.reminders.choices import INTERVAL_CHOICES
from glitter.reminders.models import Reminder


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class ReminderModelTestCase(TestCase):

    def test_intervals_data(self):
        """
        Test interval make sure if new interval added we can easily get new timedelta for
        created interval.
        """
        for interval_id in dict(INTERVAL_CHOICES).keys():
            reminder = Reminder(interval=interval_id, content_type_id=1)
            self.assertIsInstance(
                reminder.get_interval_timedelta(), datetime.timedelta
            )


class ReminderAdminTestCase(TestCase):

    @override_settings(GLITTER_PAGES_REMINDER=False)
    def test_the_inline_not_appears(self):
        """ Test to make sure inline is not set if the settings variable is not set. """
        PageAdmin.inlines = []
        page_admin = PageAdmin(model=Page, admin_site=AdminSite())
        page_admin.get_inline_instances(request)
        self.assertNotIn(ReminderInline, page_admin.inlines)

    @override_settings(GLITTER_PAGES_REMINDER=True)
    def test_the_inline_appears(self):
        """ Test to make sure inline is not set if the settings variable is not set. """
        PageAdmin.inlines = []
        page_admin = PageAdmin(model=Page, admin_site=AdminSite())
        page_admin.get_inline_instances(request)
        self.assertIn(ReminderInline, page_admin.inlines)
