import datetime

from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase, modify_settings
from django.test.client import RequestFactory

from glitter.pages.admin import PageAdmin
from glitter.pages.models import Page
from glitter.reminders.admin import ReminderInline
from glitter.reminders.choices import INTERVAL_CHOICES
from glitter.reminders.models import Reminder


class MockSuperUser(object):
    id = 10

    def has_perm(self, perm):
        return True

    def has_module_perms(self, module):
        return True

    def is_active(self):
        return True

    def is_staff(self):
        return True


class ReminderModelTestCase(SimpleTestCase):

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


class ReminderAdminTestCase(SimpleTestCase):

    def setUp(self):
        self.request = RequestFactory().request()
        self.request.user = MockSuperUser()

    @modify_settings(INSTALLED_APPS={
        'remove': 'glitter.reminders',
    })
    def test_the_inline_not_appears(self):
        """ Test to make sure inline is not set if the settings variable is not set. """
        page_admin = PageAdmin(model=Page, admin_site=AdminSite())
        data = page_admin.changeform_view(self.request, object_id=None)
        inlines = [
            formset.opts.__class__ for formset in data.context_data['inline_admin_formsets']
        ]
        self.assertNotIn(ReminderInline, inlines)

    @modify_settings(INSTALLED_APPS={
        'append': 'glitter.reminders',
    })
    def test_the_inline_appears(self):
        """ Test to make sure inline is not set if the settings variable is not set. """
        page_admin = PageAdmin(model=Page, admin_site=AdminSite())
        data = page_admin.changeform_view(self.request, object_id=None)
        inlines = [
            formset.opts.__class__ for formset in data.context_data['inline_admin_formsets']
        ]
        self.assertIn(ReminderInline, inlines)
