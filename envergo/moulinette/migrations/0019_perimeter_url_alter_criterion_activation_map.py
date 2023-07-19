# Generated by Django 4.2 on 2023-07-17 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("geodata", "0003_map_geometry"),
        ("moulinette", "0018_remove_criterion_map_caption_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="perimeter",
            name="url",
            field=models.URLField(default="https://example.org", verbose_name="Url"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="criterion",
            name="activation_map",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="criteria",
                to="geodata.map",
                verbose_name="Activation map",
            ),
        ),
    ]
