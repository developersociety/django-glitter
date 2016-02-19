# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.assets.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
        ('glitter_assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', models.CharField(blank=True, help_text='Used as ALT text', max_length=200)),
                ('caption', models.CharField(blank=True, help_text='Shown below the image', max_length=200)),
                ('link', models.URLField(blank=True)),
                ('new_window', models.BooleanField(verbose_name='Open link in new window', default=False)),
                ('content_block', models.ForeignKey(null=True, to='glitter.ContentBlock', editable=False)),
                ('image', glitter.assets.fields.AssetForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, to='glitter_assets.Image')),
            ],
            options={
                'verbose_name': 'image',
            },
        ),
    ]
