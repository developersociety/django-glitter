# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_pages', '0001_initial'),
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactFormBlock',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('recipient', models.EmailField(max_length=254)),
                ('content_block', models.ForeignKey(editable=False, null=True, to='glitter.ContentBlock')),
                ('success_page', mptt.fields.TreeForeignKey(null=True, to='glitter_pages.Page', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'contact form',
            },
        ),
    ]
