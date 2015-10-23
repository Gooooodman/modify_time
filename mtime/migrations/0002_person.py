# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mtime', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('shirt_size', models.CharField(max_length=1, choices=[(b'S', b'Small'), (b'M', b'Medium'), (b'L', b'Large')])),
            ],
        ),
    ]
