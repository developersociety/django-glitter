# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleInline',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SampleModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('content', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SampleModelWithInlinesBlock',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('content_block', models.ForeignKey(null=True, editable=False, to='glitter.ContentBlock')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sampleinline',
            name='foreign_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sampleblocks.SampleModel'),
        ),
        migrations.AddField(
            model_name='sampleinline',
            name='parent_block',
            field=models.ForeignKey(to='sampleblocks.SampleModelWithInlinesBlock'),
        ),
    ]
