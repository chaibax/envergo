# Generated by Django 3.2.6 on 2021-11-04 14:14

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0007_alter_zone_polygon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zone',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857),
        ),
    ]