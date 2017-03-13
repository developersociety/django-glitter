from celery import shared_task

from .utils import process_actions


@shared_task
def publish_task(pk=None):
    """
    Process a publish task from Celery.

    Can be given the ID of a task to action, or process all scheduled actions which need actioning.
    """
    action_ids = None

    if pk is not None:
        action_ids = [pk]

    process_actions(action_ids=action_ids)
