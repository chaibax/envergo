# Generated by Django 3.2.16 on 2023-02-28 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0031_alter_map_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='copy_to_staging',
            field=models.BooleanField(default=False, verbose_name='Copy to staging?'),
        ),
    ]
