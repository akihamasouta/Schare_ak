# Generated by Django 2.2.7 on 2020-04-12 00:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share_calendar', '0004_talk_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='for_friend', to=settings.AUTH_USER_MODEL),
        ),
    ]
