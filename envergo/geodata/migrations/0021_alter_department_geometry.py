# Generated by Django 3.2.12 on 2022-03-28 08:40

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0020_auto_20220328_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]