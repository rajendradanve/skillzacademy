# Generated by Django 3.2.8 on 2021-11-25 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='5B6FF1AA73', editable=False, max_length=10, unique=True),
        ),
    ]
