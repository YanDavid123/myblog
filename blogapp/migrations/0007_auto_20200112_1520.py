# Generated by Django 2.2.3 on 2020-01-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_auto_20200105_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=50, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='blogtype',
            name='type_name',
            field=models.CharField(max_length=15, verbose_name='博客类别'),
        ),
    ]