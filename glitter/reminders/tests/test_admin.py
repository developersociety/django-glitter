import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from django.core import management

from glitter.models import Version
from glitter.pages.models import Page
from glitter.pages.admin import PageAdmin
from glitter.reminders.admin import ReminderInline
from glitter.reminders.choices import INTERVAL_CHOICES
from glitter.reminders.models import Reminder

from .admin import site as admin_site


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


@override_settings(
    DEBUG=True,
    ROOT_URLCONF='glitter.reminders.tests.urls',
    DEBUG_TOOLBAR_PATCH_SETTINGS=False,
)
class ReminderAdminTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser_password = 'secret'
        cls.superuser_username = 'super'
        cls.superuser_email = 'test@test.com'
        cls.superuser = get_user_model().objects.create_superuser(
            username=cls.superuser_username,
            password=cls.superuser_password,
            email=cls.superuser_email
        )

    def create_page_with_version(self):
        self.page = Page.objects.create(url='/test/', title='Test page')
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page), object_id=self.page.id,
            template_name='glitter/sample.html', owner=self.superuser
        )
        self.page_version.generate_version()
        self.page.current_version = self.page_version
        self.page.save()

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

    @override_settings(GLITTER_PAGES_REMINDER=False)
    def test_basic_no_reminder_add_GET(self):
        """
        Make sure no initial data is not set for the user on the inlines and make settings
        flag is working correctly.
        """
        page_admin = PageAdmin(model=Page, admin_site=admin_site)
        page_admin.get_inline_instances(request)
        self.assertNotIn(ReminderInline, page_admin.inlines)

    @override_settings(GLITTER_PAGES_REMINDER=True)
    def test_basic_with_reminder_add_GET(self):
        """
        Make sure no initial data is not set for the user on the inlines and make settings
        flag is working correctly.
        """
        page_admin = PageAdmin(model=Page, admin_site=admin_site)
        page_admin.get_inline_instances(request)
        self.assertIn(ReminderInline, page_admin.inlines)

    def test_initial_data(self):
        """
        Check if user initial data been passed to the formset if page current object exists.
        """
        self.create_page_with_version()

        inline = ReminderInline(Page, admin_site)
        formset = inline.get_formset(request, self.page)
        self.assertEqual(
            formset.form.base_fields['user'].initial, self.page.current_version.owner.id
        )
