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
            name='Banner',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('link', models.URLField()),
                ('link_text', models.CharField(blank=True, max_length=100)),
                ('new_window', models.BooleanField(verbose_name='Open link in new window', default=False)),
                ('image', glitter.assets.fields.AssetForeignKey(blank=True, null=True, to='glitter_assets.Image')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='BannerBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('content_block', models.ForeignKey(null=True, to='glitter.ContentBlock', editable=False)),
            ],
            options={
                'verbose_name': 'banner',
            },
        ),
        migrations.CreateModel(
            name='BannerInline',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('banner', models.ForeignKey(to='glitter_banner.Banner', on_delete=django.db.models.deletion.PROTECT)),
                ('banner_block', models.ForeignKey(to='glitter_banner.BannerBlock')),
            ],
            options={
                'verbose_name': 'banner',
                'ordering': ('id',),
            },
        ),
    ]
