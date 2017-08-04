from django.db import models


class FileMixin(models.Model):
    class Meta:
        abstract = True
        ordering = ('-created_at', '-modified_at', 'title')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.file.url

    def save(self, *args, **kwargs):
        # Avoid doing file size requests constantly
        self.file_size = self.file.size

        super().save(*args, **kwargs)
