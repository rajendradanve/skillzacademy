# Generated by Django 3.2.8 on 2022-01-14 01:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_alter_course_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='number_of_lectures',
        ),
        migrations.AlterField(
            model_name='course',
            name='date_updated',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='time_updated',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='date_updated',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='time_updated',
            field=models.TimeField(default=django.utils.timezone.now, null=True),
        ),
    ]