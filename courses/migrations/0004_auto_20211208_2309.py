# Generated by Django 3.2.8 on 2021-12-08 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_courseschedule_course_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseschedule',
            name='course_timezone',
        ),
        migrations.AddField(
            model_name='course',
            name='course_timezone',
            field=models.CharField(default='CET', max_length=100),
        ),
    ]