# Generated by Django 4.2 on 2023-07-13 09:32

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("moulinette", "0013_remove_regulation_activation_distance_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="criterion",
            old_name="perimeter",
            new_name="activation_map",
        ),
        migrations.RenameField(
            model_name="perimeter",
            old_name="map",
            new_name="activation_map",
        ),
        migrations.RemoveField(
            model_name="perimeter",
            name="criterion",
        ),
        migrations.AddField(
            model_name="perimeter",
            name="contact_phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None, verbose_name="Contact phone"
            ),
        ),
        migrations.AddField(
            model_name="perimeter",
            name="contact_url",
            field=models.URLField(blank=True, verbose_name="Contact url"),
        ),
        migrations.AddField(
            model_name="perimeter",
            name="regulation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="perimeters",
                to="moulinette.regulation",
                verbose_name="Regulation",
            ),
            preserve_default=False,
        ),
    ]