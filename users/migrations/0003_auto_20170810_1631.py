# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 20:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170810_1426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='user_fk',
        ),
    ]
