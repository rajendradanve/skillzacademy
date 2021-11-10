# Generated by Django 3.2.8 on 2021-11-10 18:40

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20211110_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='for_whom',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor_info',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='learning_objectives',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='prerequisite',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
