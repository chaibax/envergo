# Generated by Django 3.2.6 on 2021-11-09 08:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0009_alter_zone_polygon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zone',
            old_name='polygon',
            new_name='geometry',
        ),
        migrations.RemoveField(
            model_name='zone',
            name='code',
        ),
        migrations.AddField(
            model_name='zone',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AddField(
            model_name='zone',
            name='data',
            field=models.JSONField(null=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='zone',
            name='name',
            field=models.CharField(default='', max_length=256, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zone',
            name='source_url',
            field=models.URLField(null=True, verbose_name='Source url'),
        ),
    ]