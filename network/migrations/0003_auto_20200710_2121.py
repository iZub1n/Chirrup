# Generated by Django 3.0.8 on 2020-07-10 21:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20200710_0214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='dT',
            new_name='dTCreated',
        ),
        migrations.AddField(
            model_name='post',
            name='dtEdited',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='_user_followers_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]