# Generated by Django 4.2 on 2023-09-07 08:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("evaluations", "0014_remove_maillog_subject_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="regulatorynoticelog",
            name="last_clicked",
        ),
        migrations.RemoveField(
            model_name="regulatorynoticelog",
            name="last_opened",
        ),
        migrations.RemoveField(
            model_name="regulatorynoticelog",
            name="nb_clicked",
        ),
        migrations.RemoveField(
            model_name="regulatorynoticelog",
            name="nb_opened",
        ),
    ]