# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime
import ww.api.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('method', models.CharField(max_length=10, blank=True)),
                ('user_agent', models.CharField(max_length=255, blank=True)),
                ('remote_addr', models.GenericIPAddressField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('word', models.CharField(default=ww.api.models.watchword, unique=True, max_length=10, editable=False)),
                ('cycle', models.DurationField(default=datetime.timedelta(1))),
                ('grace', models.DurationField(default=datetime.timedelta(0, 3600))),
                ('state', models.CharField(default=b'fresh', max_length=5, choices=[(b'fresh', b'Fresh'), (b'quiet', b'Quiet'), (b'alert', b'Alert'), (b'alarm', b'Alarm'), (b'sleep', b'Sleep')])),
                ('last_ping', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ping',
            name='watch',
            field=models.ForeignKey(to='api.Watch', on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
