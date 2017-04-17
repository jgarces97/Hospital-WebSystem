# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-03 19:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HNApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('start', models.TimeField(verbose_name='Start Time')),
                ('end', models.TimeField(verbose_name='End Time')),
                ('title', models.CharField(max_length=20)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HNApp.DoctorModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
