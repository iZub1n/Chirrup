# Generated by Django 3.0.8 on 2020-07-24 22:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_reaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='type',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(0)]),
        ),
    ]
