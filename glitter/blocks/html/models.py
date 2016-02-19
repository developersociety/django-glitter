from django.db import models

from glitter.models import BaseBlock


class HTML(BaseBlock):
    content = models.TextField()

    class Meta:
        verbose_name = 'HTML'
