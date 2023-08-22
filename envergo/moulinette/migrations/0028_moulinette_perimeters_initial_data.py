# Generated by Django 4.2 on 2023-07-19 12:41

from django.db import migrations, transaction
from django.core.management import call_command


@transaction.atomic
def create_initial_data(apps, schema_editor):
    MoulinetteConfig = apps.get_model("moulinette", "MoulinetteConfig")
    MoulinetteConfig.objects.all().delete()

    Perimeter = apps.get_model("moulinette", "Perimeter")
    Perimeter.objects.all().delete()

    call_command("loaddata", "envergo/moulinette/migrations/moulinette_sage.json")


class Migration(migrations.Migration):
    dependencies = [
        ("moulinette", "0027_alter_perimeter_url"),
    ]

    # operations = [
    #     migrations.RunSQL(
    #         """
    #         ALTER TABLE moulinette_perimeter
    #         DROP IF EXISTS criterion
    #         """,
    #         migrations.RunSQL.noop,
    #     ),
    #     migrations.RunPython(create_initial_data, migrations.RunPython.noop),
    # ]
