# Generated by Django 2.2.7 on 2020-06-04 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share_calendar', '0017_balloon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='schedule',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='share_calendar.Schedule'),
        ),
    ]
