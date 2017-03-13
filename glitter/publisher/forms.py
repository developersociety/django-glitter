from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import BLANK_CHOICE_DASH

from glitter.models import Version

from .models import PublishAction


def object_version_choices(obj):
    """
    Return a list of form choices for versions of this object which can be published.
    """
    choices = BLANK_CHOICE_DASH + [(PublishAction.UNPUBLISH_CHOICE, 'Unpublish current version')]

    # When creating a new object in the Django admin - obj will be None
    if obj is not None:
        saved_versions = Version.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
        ).exclude(
            version_number=None,
        )

        for version in saved_versions:
            choices.append((version.version_number, version))

    return choices
