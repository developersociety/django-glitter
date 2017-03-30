from django import forms

from .models import Reminder


class ReminderInlineAdminForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ('user', 'interval', 'object_id', 'content_type',)

    def clean_user(self):
        user = self.cleaned_data['user']
        if not user.email:
            raise forms.ValidationError(
                "User doesn't have an email address, please pick a different user or add an "
                "email address"
            )
        return user

    def validate_unique(self):
        """
        Add this method because django doesn't validate correctly because required fields are
        excluded.
        """
        unique_checks, date_checks = self.instance._get_unique_checks(exclude=[])
        errors = self.instance._perform_unique_checks(unique_checks)
        if errors:
            self.add_error(None, errors)
