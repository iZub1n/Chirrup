# Generated by Django 3.0.8 on 2020-07-25 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_auto_20200724_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='network.Post'),
        ),
    ]