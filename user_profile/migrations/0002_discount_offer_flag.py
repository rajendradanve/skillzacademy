# Generated by Django 3.2.8 on 2021-12-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='offer_flag',
            field=models.BooleanField(default=False),
        ),
    ]
