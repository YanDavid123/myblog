# Generated by Django 2.2.3 on 2019-10-27 08:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0002_readdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 10, 27, 8, 5, 25, 417880, tzinfo=utc)),
        ),
    ]
