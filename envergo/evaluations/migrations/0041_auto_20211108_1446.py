# Generated by Django 3.2.6 on 2021-11-08 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0040_remove_evaluation_commune'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='details_html',
            field=models.TextField(blank=True, verbose_name='Details'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='details_md',
            field=models.TextField(blank=True, verbose_name='Details'),
        ),
    ]