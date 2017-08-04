from django.db import models


class BaseImageBlockManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('image')
