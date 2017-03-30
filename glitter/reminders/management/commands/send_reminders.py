from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from glitter.reminders.models import Reminder


class Command(BaseCommand):
    help = 'Management command to send reminder about out dated content.'

    def handle(self, *args, **options):

        self.verbosity = options.get('verbosity')

        for reminder in Reminder.objects.select_related(
                'content_type'
        ).exclude(
            user__email=''
        ).iterator():
            content_obj = reminder.content_object

            if content_obj.current_version and content_obj.published:

                date_difference = timezone.now() - content_obj.current_version.modified
                reminder_difference = timezone.now() - reminder.sent_at

                if (
                        date_difference >= reminder.get_interval_timedelta() and
                        reminder_difference >= reminder.get_interval_timedelta()
                ):

                    current_site = Site.objects.get_current()

                    send_mail(
                        subject='{site_name} - Outdated content for {model}'.format(
                            site_name=current_site.name,
                            model=content_obj._meta.model_name.title(),
                        ),
                        message=(
                            'Please update the outdated content for {model} '
                            'https://{domain}{url}'.format(
                                model=content_obj._meta.model_name.title(),
                                domain=current_site.domain,
                                url=content_obj.get_absolute_url(),
                            )
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[reminder.user.email],
                    )
                    self.stdout.write(
                        'Email for {} is sent to: {}'.format(content_obj, reminder.user.email)
                    )
                    # Update the updated_at date to make sure it's not get send reminders.
                    reminder.sent_at = timezone.now()
                    reminder.save()
                else:
                    if self.verbosity == 3:
                        self.stdout.write(
                            'Email for {} is not sent to: {}'.format(
                                content_obj, reminder.user.email
                            )
                        )
