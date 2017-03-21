from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from glitter.models import Version
from glitter.pages.models import Page
from glitter.reminders.admin import ReminderInline


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

    def test_initial_data(self):
        """
        Check if user initial data been passed to the formset if page current object exists.
        """
        self.create_page_with_version()

        inline = ReminderInline(Page, AdminSite())
        formset = inline.get_formset(request, self.page)
        self.assertEqual(
            formset.form.base_fields['user'].initial, self.page.current_version.owner.id
        )
