# Generated by Django 2.2.3 on 2019-11-14 13:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Conment',
            new_name='Comment',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='content_time',
            new_name='comment_time',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='content_user',
            new_name='comment_user',
        ),
    ]
