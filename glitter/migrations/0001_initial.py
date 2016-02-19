# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentBlock',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('column', models.CharField(db_index=True, max_length=100)),
                ('position', models.IntegerField(db_index=True, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='+')),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('version_number', models.PositiveIntegerField(db_index=True, null=True)),
                ('template_name', models.CharField(max_length=70)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'ordering': ('-version_number',),
            },
        ),
        migrations.AddField(
            model_name='contentblock',
            name='obj_version',
            field=models.ForeignKey(to='glitter.Version'),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('content_type', 'object_id', 'version_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='contentblock',
            unique_together=set([('obj_version', 'column', 'position')]),
        ),
    ]
