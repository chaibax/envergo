# Generated by Django 4.2 on 2023-07-17 08:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("moulinette", "0017_perimeter_long_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="criterion",
            name="map_caption",
        ),
        migrations.RemoveField(
            model_name="criterion",
            name="polygon_color",
        ),
        migrations.RemoveField(
            model_name="criterion",
            name="show_map",
        ),
        migrations.RemoveField(
            model_name="regulation",
            name="map_caption",
        ),
        migrations.AlterField(
            model_name="regulation",
            name="show_map",
            field=models.BooleanField(
                default=False,
                help_text="The perimeter's map will be displayed, if it exists",
                verbose_name="Show perimeter map",
            ),
        ),
    ]
