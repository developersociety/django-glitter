# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.assets.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_image', '0003_delete_empty_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageblock',
            name='image',
            field=glitter.assets.fields.AssetForeignKey(on_delete=django.db.models.deletion.PROTECT, to='glitter_assets.Image'),
        ),
    ]
