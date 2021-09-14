# Generated by Django 3.2.6 on 2021-08-27 09:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='commune',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(message='The code must be a 5-digit number', regex='^[\\d]{5}$')], verbose_name='Commune INSEE code'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='order',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(limit_value=9999, message='The parcel must be a number between 1 and 9999')], verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='prefix',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(message='The prefix must be a 3-digit number.', regex='^[\\d]{3}$')], verbose_name='Prefix'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='section',
            field=models.CharField(max_length=2, validators=[django.core.validators.RegexValidator(message='The section must be one or two uppercase letters.', regex='^[0A-Z][A-Z]$')], verbose_name='Section letter(s)'),
        ),
    ]