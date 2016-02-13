# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('config', models.CharField(max_length=255, blank=True)),
                ('signal', models.CharField(default=b'email', max_length=10, choices=[(b'email', b'Email'), (b'webhook', b'Webhook')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Launch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(max_length=255, blank=True)),
                ('trigger_state', models.CharField(max_length=5, choices=[(b'fresh', b'Fresh'), (b'quiet', b'Quiet'), (b'alert', b'Alert'), (b'alarm', b'Alarm'), (b'sleep', b'Sleep')])),
                ('flare', models.ForeignKey(to='api.Flare')),
                ('watch', models.ForeignKey(to='api.Watch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='watch',
            name='flares',
            field=models.ManyToManyField(to='api.Flare'),
        ),
    ]
