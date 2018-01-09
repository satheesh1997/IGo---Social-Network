# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 13:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0009_education_is_studying'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=500)),
                ('upload_image', models.URLField(default=None)),
                ('upload_video', models.URLField(default=None)),
                ('upload_location', models.CharField(default=None, max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='dp',
            field=models.URLField(default='http://techtrendz.in/uploads/a1df072abf2a58cfa0bd90fce5a0b65eac9e4952e7dc8c1b1dd05c24bfdb3947/images/default.png'),
        ),
    ]