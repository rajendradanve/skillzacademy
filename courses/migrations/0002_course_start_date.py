# Generated by Django 3.2.8 on 2021-12-08 22:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]