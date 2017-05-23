# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import glitter.assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_text_image', '0002_delete_empty_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textimageblock',
            name='image',
            field=glitter.assets.fields.AssetForeignKey(on_delete=django.db.models.deletion.PROTECT, to='glitter_assets.Image'),
        ),
    ]
