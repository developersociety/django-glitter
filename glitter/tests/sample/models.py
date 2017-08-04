from django.db import models

from glitter.mixins import GlitterMixin


class Book(GlitterMixin):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
