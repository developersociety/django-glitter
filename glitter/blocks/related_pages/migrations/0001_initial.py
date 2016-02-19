# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
        ('glitter_pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedPage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='Optional for pages, required for links', blank=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=0, db_index=True)),
                ('page', mptt.fields.TreeForeignKey(blank=True, null=True, to='glitter_pages.Page')),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='RelatedPagesBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='Defaults to "Related pages"', blank=True)),
                ('content_block', models.ForeignKey(null=True, editable=False, to='glitter.ContentBlock')),
            ],
            options={
                'verbose_name': 'related pages',
            },
        ),
        migrations.AddField(
            model_name='relatedpage',
            name='related_pages_block',
            field=models.ForeignKey(to='glitter_related_pages.RelatedPagesBlock'),
        ),
    ]
