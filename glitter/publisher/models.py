from __future__ import unicode_literals

from django.conf import settings
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible

from glitter.models import Version

from .validators import future_date


@python_2_unicode_compatible
class PublishAction(models.Model):
    UNPUBLISH_CHOICE = -1

    # The glittered object we're linked to
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # When/what we're updating, and by who
    scheduled_time = models.DateTimeField(validators=[future_date])
    publish_version = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Scheduled publishing'
        ordering = ('scheduled_time', 'id')

    def __str__(self):
        if self.publish_version == self.UNPUBLISH_CHOICE:
            return 'Unpublish at {}'.format(self.scheduled_time)
        else:
            return 'Publish version {} at {}'.format(self.publish_version, self.scheduled_time)

    def save(self, *args, **kwargs):
        super(PublishAction, self).save(*args, **kwargs)

        # Add a task
        if self.can_schedule_task():
            self.schedule_task()

    def can_schedule_task(self):
        """
        Can task sched
        """
        from .utils import celery_enabled  # avoid a circular import

        tasks_enabled = celery_enabled()
        return tasks_enabled

    def schedule_task(self):
        """
        Schedules this publish action as a Celery task.
        """
        from .tasks import publish_task

        publish_task.apply_async(kwargs={'pk': self.pk}, eta=self.scheduled_time)

    def get_version(self):
        """
        Get the version object for the related object.
        """
        return Version.objects.get(
            content_type=self.content_type,
            object_id=self.object_id,
            version_number=self.publish_version,
        )

    def _publish(self):
        """
        Process a publish action on the related object, returns a boolean if a change is made.

        Only objects where a version change is needed will be updated.
        """
        obj = self.content_object
        version = self.get_version()
        actioned = False

        # Only update if needed
        if obj.current_version != version:
            version = self.get_version()
            obj.current_version = version
            obj.save(update_fields=['current_version'])
            actioned = True

        return actioned

    def _unpublish(self):
        """
        Process an unpublish action on the related object, returns a boolean if a change is made.

        Only objects with a current active version will be updated.
        """
        obj = self.content_object
        actioned = False

        # Only update if needed
        if obj.current_version is not None:
            obj.current_version = None
            obj.save(update_fields=['current_version'])
            actioned = True

        return actioned

    def _log_action(self):
        """
        Adds a log entry for this action to the object history in the Django admin.
        """
        if self.publish_version == self.UNPUBLISH_CHOICE:
            message = 'Unpublished page (scheduled)'
        else:
            message = 'Published version {} (scheduled)'.format(self.publish_version)

        LogEntry.objects.log_action(
            user_id=self.user.pk,
            content_type_id=self.content_type.pk,
            object_id=self.object_id,
            object_repr=force_text(self.content_object),
            action_flag=CHANGE,
            change_message=message
        )

    def process_action(self):
        """
        Process the action and update the related object, returns a boolean if a change is made.
        """
        if self.publish_version == self.UNPUBLISH_CHOICE:
            actioned = self._unpublish()
        else:
            actioned = self._publish()

        # Only log if an action was actually taken
        if actioned:
            self._log_action()

        return actioned
