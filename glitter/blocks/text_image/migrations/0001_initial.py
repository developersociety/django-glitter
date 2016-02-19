# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import glitter.assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
        ('glitter_assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextImageBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('content_block', models.ForeignKey(to='glitter.ContentBlock', null=True, editable=False)),
                ('image', glitter.assets.fields.AssetForeignKey(to='glitter_assets.Image', null=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Text/Image',
            },
        ),
    ]
