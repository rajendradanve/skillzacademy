# Generated by Django 3.2.8 on 2021-12-08 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='2C9791119C', editable=False, max_length=10, unique=True),
        ),
    ]
