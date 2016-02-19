# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import glitter.pages.validators


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('published', models.BooleanField(default=True, db_index=True)),
                ('url', models.CharField(verbose_name='URL', validators=[glitter.pages.validators.validate_page_url], max_length=100, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('login_required', models.BooleanField(default=False)),
                ('show_in_navigation', models.BooleanField(default=True, db_index=True)),
                ('unpublished_count', models.PositiveIntegerField(default=0, editable=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('current_version', models.ForeignKey(blank=True, editable=False, to='glitter.Version', null=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='glitter_pages.Page', null=True, related_name='children')),
            ],
            options={
                'verbose_name': 'page',
                'ordering': ('url',),
                'default_permissions': ('add', 'change', 'delete', 'edit', 'publish'),
                'abstract': False,
                'permissions': (('view_protected_page', 'Can view protected page'),),
            },
        ),
    ]
