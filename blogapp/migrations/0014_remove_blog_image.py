# Generated by Django 2.2.3 on 2020-03-05 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0013_auto_20200305_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='image',
        ),
    ]
