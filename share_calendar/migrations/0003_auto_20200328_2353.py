# Generated by Django 2.2.7 on 2020-03-28 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_calendar', '0002_auto_20200328_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member',
            field=models.ManyToManyField(default='', to='share_calendar.Friend'),
        ),
    ]
