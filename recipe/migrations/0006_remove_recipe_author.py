# Generated by Django 3.2.6 on 2021-08-20 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20210820_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='author',
        ),
    ]
