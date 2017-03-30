from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import mark_safe

from .forms import ReminderInlineAdminForm
from .models import Reminder


class ReminderInline(GenericTabularInline):
    raw_id_fields = ('user',)
    model = Reminder
    form = ReminderInlineAdminForm
    verbose_name_plural = mark_safe('Reminder <small>(to update the content)</small>')
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        """ Default user to the current version owner. """
        data = super(ReminderInline, self).get_formset(request, obj, **kwargs)
        if obj:
            data.form.base_fields['user'].initial = request.user.id
        return data
