from __future__ import unicode_literals

from django import forms
from django.contrib.contenttypes.admin import GenericStackedInline

from .forms import object_version_choices
from .models import PublishAction


class ActionInline(GenericStackedInline):
    model = PublishAction
    fields = ('scheduled_time', 'publish_version')
    extra = 0

    def get_formset(self, request, obj=None, form=None, **kwargs):
        class VersionForm(forms.ModelForm):
            """
            Customised form which limits the users choices to versions which have been saved for
            this object.
            """
            class Meta:
                widgets = {
                    'publish_version': forms.widgets.Select(
                        choices=object_version_choices(obj=obj),
                    ),
                }

        BaseFormset = super(ActionInline, self).get_formset(
            request, obj, form=VersionForm, **kwargs
        )

        class ActionFormset(BaseFormset):
            """
            Customised formset to save the user who has created/updated the action.
            """
            def save_new(self, form, commit):
                obj = super(ActionFormset, self).save_new(form, commit=False)
                obj.user = request.user
                obj.save()
                return obj

            def save_existing(self, form, instance, commit):
                obj = super(ActionFormset, self).save_existing(form, instance, commit=False)
                obj.user = request.user
                obj.save()
                return obj

        return ActionFormset
