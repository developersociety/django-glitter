# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefinitionList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('content_block', models.ForeignKey(editable=False, to='glitter.ContentBlock', null=True)),
            ],
            options={
                'verbose_name': 'Definition list',
            },
        ),
        migrations.CreateModel(
            name='DefinitionListInline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=128)),
                ('value', models.TextField()),
                ('definition_list', models.ForeignKey(to='glitter_definition_list.DefinitionList')),
            ],
        ),
    ]
