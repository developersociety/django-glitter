from django import forms

from .models import Reminder


class ReminderInlineAdminForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ('user', 'interval',)

    def clean_user(self):
        user = self.cleaned_data['user']
        if not user.email:
            raise forms.ValidationError(
                "{} - don't have email address please pick different user or enter "
                "the email address.".format(user)
            )
        return user
