# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_empty_blocks(apps, schema_editor):
    BannerBlock = apps.get_model('glitter_banner', 'BannerBlock')
    ContentBlock = apps.get_model('glitter', 'ContentBlock')

    empty_blocks = BannerBlock.objects.filter(bannerinline=None)
    content_block_ids = empty_blocks.values_list('content_block_id', flat=True)

    ContentBlock.objects.filter(id__in=content_block_ids).delete()
    empty_blocks.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_banner', '0003_make_banner_link_optional'),
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_empty_blocks, reverse_code=migrations.RunPython.noop),
    ]
