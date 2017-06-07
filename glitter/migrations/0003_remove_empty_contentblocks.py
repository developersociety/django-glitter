# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_empty_blocks(apps, schema_editor):
    ContentBlock = apps.get_model('glitter', 'ContentBlock')
    ContentBlock.objects.filter(object_id=None).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0002_object_id_not_required'),
    ]

    operations = [
        migrations.RunPython(remove_empty_blocks, reverse_code=migrations.RunPython.noop),
    ]
