# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_empty_blocks(apps, schema_editor):
    CarouselBlock = apps.get_model('glitter_carousel', 'CarouselBlock')
    ContentBlock = apps.get_model('glitter', 'ContentBlock')

    empty_blocks = CarouselBlock.objects.filter(carousel=None)
    content_block_ids = empty_blocks.values_list('content_block_id', flat=True)

    ContentBlock.objects.filter(id__in=content_block_ids).delete()
    empty_blocks.delete()

    ImageOnlyCarouselBlock = apps.get_model('glitter_carousel', 'ImageOnlyCarouselBlock')
    ContentBlock = apps.get_model('glitter', 'ContentBlock')

    empty_blocks = ImageOnlyCarouselBlock.objects.filter(carousel=None)
    content_block_ids = empty_blocks.values_list('content_block_id', flat=True)

    ContentBlock.objects.filter(id__in=content_block_ids).delete()
    empty_blocks.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_carousel', '0003_subtitle_textfield'),
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_empty_blocks, reverse_code=migrations.RunPython.noop),
    ]
