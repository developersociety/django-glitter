# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations, models


def loadfixture(apps, schema_editor):
    call_command('loaddata', 'languages.json')


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('iso_1_code', models.CharField(max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(loadfixture),
        migrations.AddField(
            model_name='page',
            name='language',
            field=models.ForeignKey(to='glitter_pages.Language', default=38, blank=True, null=True),
        ),
    ]
