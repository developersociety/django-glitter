from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from glitter.models import Version
from glitter.pages.models import Page
from glitter.reminders.admin import ReminderInline


class MockRequest(object):
    pass


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


@override_settings(
    ROOT_URLCONF='glitter.reminders.tests.urls',
)
class ReminderAdminTestCase(TestCase):

    def setUp(self):
        self.request = MockRequest()
        self.request.user = MockSuperUser()

    @classmethod
    def setUpTestData(cls):
        cls.superuser_password = 'secret'
        cls.superuser_username = 'super'
        cls.superuser_email = 'test@test.com'
        cls.superuser = User.objects.create_superuser(
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

    def test_initial_data(self):
        """
        Check if user initial data been passed to the formset if page current object exists.
        """
        self.create_page_with_version()

        inline = ReminderInline(Page, AdminSite())
        formset = inline.get_formset(self.request, self.page)
        self.assertEqual(
            formset.form.base_fields['user'].initial, self.request.user.id
        )
