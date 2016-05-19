from django.db import models

from glitter.fields import LinkField
from glitter.models import BaseBlock


class CallToActionBlock(BaseBlock):
    title = models.CharField(max_length=100)
    link = LinkField()

    class Meta:
        verbose_name = 'call to action'
