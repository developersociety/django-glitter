from django.db import models

from glitter.models import BaseBlock


class CallToActionBlock(BaseBlock):
    title = models.CharField(max_length=100)
    link = models.URLField()

    class Meta:
        verbose_name = 'call to action'
