import datetime
from calendar import monthrange

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from . import choices as reminders_choices


class Reminder(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    interval = models.IntegerField(choices=reminders_choices.INTERVAL_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'object_id', 'content_type',)

    def __str__(self):
        return '{model} {obj} interval - {interval}'.format(
            model=self.content_type.model.title(),
            obj=self.content_object,
            interval=self.get_interval_display(),
        )

    def get_interval_timedelta(self):
        """ Spits out the timedelta in days. """

        now_datetime = timezone.now()
        current_month_days = monthrange(now_datetime.year, now_datetime.month)[1]

        # Two weeks
        if self.interval == reminders_choices.INTERVAL_2_WEEKS:
            interval_timedelta = datetime.timedelta(days=14)

        # One month
        elif self.interval == reminders_choices.INTERVAL_ONE_MONTH:
            interval_timedelta = datetime.timedelta(days=current_month_days)

        # Three months
        elif self.interval == reminders_choices.INTERVAL_THREE_MONTHS:
            three_months = now_datetime + relativedelta(months=+3)
            interval_timedelta = three_months - now_datetime

        # Six months
        elif self.interval == reminders_choices.INTERVAL_SIX_MONTHS:
            six_months = now_datetime + relativedelta(months=+6)
            interval_timedelta = six_months - now_datetime

        # One year
        elif self.interval == reminders_choices.INTERVAL_ONE_YEAR:
            one_year = now_datetime + relativedelta(years=+1)
            interval_timedelta = one_year - now_datetime

        return interval_timedelta
