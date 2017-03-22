# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('glitter', '0002_object_id_not_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('interval', models.IntegerField(choices=[(1, 'Every 2 weeks'), (2, 'Every month'), (3, 'Every 3 months'), (4, 'Every 6 months'), (5, 'Every year')])),
                ('sent_at', models.DateTimeField(null=True, auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='reminder',
            unique_together=set([('user', 'object_id', 'content_type')]),
        ),
    ]
