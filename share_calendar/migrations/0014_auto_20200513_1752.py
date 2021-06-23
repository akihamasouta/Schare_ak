# Generated by Django 2.2.7 on 2020-05-13 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share_calendar', '0013_auto_20200513_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='Today_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos')),
            ],
        ),
        migrations.RemoveField(
            model_name='today',
            name='content',
        ),
        migrations.AlterField(
            model_name='today',
            name='sc_title',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='share_calendar.Schedule'),
        ),
    ]
