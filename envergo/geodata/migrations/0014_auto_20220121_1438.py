# Generated by Django 3.2.11 on 2022-01-21 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0013_map_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zone',
            name='data',
        ),
        migrations.RemoveField(
            model_name='zone',
            name='name',
        ),
    ]