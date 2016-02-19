# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.assets.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_assets', '0001_initial'),
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
            ],
            options={
                'abstract': False,
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='CarouselBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('carousel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, to='glitter_carousel.Carousel')),
                ('content_block', models.ForeignKey(null=True, to='glitter.ContentBlock', editable=False)),
            ],
            options={
                'verbose_name': 'carousel',
            },
        ),
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(blank=True, max_length=100)),
                ('link', models.URLField()),
                ('carousel', models.ForeignKey(related_name='carousel_images', to='glitter_carousel.Carousel')),
                ('image', glitter.assets.fields.AssetForeignKey(on_delete=django.db.models.deletion.PROTECT, to='glitter_assets.Image')),
            ],
            options={
                'abstract': False,
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ImageOnlyCarousel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
            ],
            options={
                'abstract': False,
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='ImageOnlyCarouselBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('carousel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, to='glitter_carousel.ImageOnlyCarousel')),
                ('content_block', models.ForeignKey(null=True, to='glitter.ContentBlock', editable=False)),
            ],
            options={
                'verbose_name': 'image only carousel',
            },
        ),
        migrations.CreateModel(
            name='ImageOnlyCarouselImage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('carousel', models.ForeignKey(related_name='carousel_images', to='glitter_carousel.ImageOnlyCarousel')),
                ('image', glitter.assets.fields.AssetForeignKey(on_delete=django.db.models.deletion.PROTECT, to='glitter_assets.Image')),
            ],
            options={
                'abstract': False,
                'ordering': ('id',),
            },
        ),
    ]
