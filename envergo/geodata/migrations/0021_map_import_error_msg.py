# Generated by Django 3.2.12 on 2022-03-23 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0020_map_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='import_error_msg',
            field=models.TextField(blank=True, verbose_name='Import error message'),
        ),
    ]