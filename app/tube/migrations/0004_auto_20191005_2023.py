# Generated by Django 2.1.12 on 2019-10-05 17:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0003_auto_20191003_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]