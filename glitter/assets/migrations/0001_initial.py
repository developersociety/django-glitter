# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('file', models.FileField(upload_to='assets/file')),
                ('file_size', models.PositiveIntegerField(default=0, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
                'ordering': ('-created_at', '-modified_at', 'title'),
            },
        ),
        migrations.CreateModel(
            name='FileCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'file categories',
                'abstract': False,
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('file', models.ImageField(width_field='image_width', upload_to='assets/image', verbose_name='Image', height_field='image_height')),
                ('image_height', models.PositiveIntegerField(editable=False)),
                ('image_width', models.PositiveIntegerField(editable=False)),
                ('file_size', models.PositiveIntegerField(default=0, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
                'ordering': ('-created_at', '-modified_at', 'title'),
            },
        ),
        migrations.CreateModel(
            name='ImageCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'image categories',
                'abstract': False,
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='image',
            name='category',
            field=models.ForeignKey(to='glitter_assets.ImageCategory'),
        ),
        migrations.AddField(
            model_name='file',
            name='category',
            field=models.ForeignKey(to='glitter_assets.FileCategory'),
        ),
    ]
