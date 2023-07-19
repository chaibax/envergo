# Generated by Django 4.2 on 2023-07-18 13:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("moulinette", "0020_perimeter_contact_email_perimeter_contact_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="criterion",
            name="weight",
            field=models.PositiveIntegerField(default=1, verbose_name="Order"),
        ),
        migrations.AlterField(
            model_name="regulation",
            name="weight",
            field=models.PositiveIntegerField(default=1, verbose_name="Order"),
        ),
    ]
