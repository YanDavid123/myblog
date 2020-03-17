# Generated by Django 2.2.3 on 2020-03-05 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0012_auto_20200305_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='avatar',
        ),
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='', upload_to='media/upload/%Y/%m/%d'),
        ),
    ]
