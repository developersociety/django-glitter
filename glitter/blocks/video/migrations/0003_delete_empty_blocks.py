# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_empty_blocks(apps, schema_editor):
    Video = apps.get_model('glitter_video', 'Video')
    ContentBlock = apps.get_model('glitter', 'ContentBlock')

    empty_blocks = Video.objects.filter(url='')
    content_block_ids = empty_blocks.values_list('content_block_id', flat=True)

    ContentBlock.objects.filter(id__in=content_block_ids).delete()
    empty_blocks.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_video', '0002_video_title'),
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_empty_blocks, reverse_code=migrations.RunPython.noop),
    ]
