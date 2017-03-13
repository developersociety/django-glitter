from __future__ import unicode_literals

from django.conf import settings
from django.utils import timezone

from .models import PublishAction


def process_actions(action_ids=None):
    """
    Process actions in the publishing schedule.

    Returns the number of actions processed.
    """
    actions_taken = 0
    action_list = PublishAction.objects.prefetch_related(
        'content_object',
    ).filter(
        scheduled_time__lte=timezone.now(),
    )

    if action_ids is not None:
        action_list = action_list.filter(id__in=action_ids)

    for action in action_list:
        action.process_action()
        action.delete()
        actions_taken += 1

    return actions_taken


def celery_enabled():
    """
    Return a boolean if Celery tasks are enabled for this app.

    If the ``GLITTER_PUBLISHER_CELERY`` setting is ``True`` or ``False`` - then that value will be
    used. However if the setting isn't defined, then this will be enabled automatically if Celery
    is installed.
    """
    enabled = getattr(settings, 'GLITTER_PUBLISHER_CELERY', None)

    if enabled is None:
        try:
            import celery  # noqa
            enabled = True
        except ImportError:
            enabled = False

    return enabled
