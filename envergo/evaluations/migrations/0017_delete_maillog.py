# Generated by Django 4.2 on 2023-09-08 12:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("evaluations", "0016_recipientstatus"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MailLog",
        ),
    ]