# Generated by Django 3.2.16 on 2023-03-15 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0032_map_copy_to_staging'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='contact_html',
        ),
        migrations.RemoveField(
            model_name='department',
            name='contact_md',
        ),
    ]