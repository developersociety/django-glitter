# -*- coding: utf-8 -*-

from django.db.models.signals import post_save

from .models import Page


def version_update(instance, raw=False, **kwargs):
    # Don't update on loaddata
    if raw:
        return

    obj = instance.content_object

    if isinstance(obj, Page):
        # Page save method recalculates the unpublished pages
        obj.save()


post_save.connect(version_update, sender='glitter.Version')
