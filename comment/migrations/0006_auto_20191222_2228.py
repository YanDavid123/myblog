# Generated by Django 2.2.3 on 2019-12-22 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20191222_2126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='reply',
            new_name='reply_to',
        ),
    ]
