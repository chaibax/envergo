# Generated by Django 4.2 on 2023-08-22 14:15

from django.db import migrations


def update_header_keys(apps, schema_editor):
    MoulinetteConfig = apps.get_model("moulinette", "MoulinetteConfig")
    for config in MoulinetteConfig.objects.all():
        values = config.criteria_values
        new_values = {}
        for key, value in values.items():
            new_key = f"natura2000__{key}"
            new_values[new_key] = value
        config.criteria_values = new_values
        config.save()


class Migration(migrations.Migration):
    dependencies = [
        ("moulinette", "0028_moulinette_perimeters_initial_data"),
    ]

    operations = [migrations.RunPython(update_header_keys)]