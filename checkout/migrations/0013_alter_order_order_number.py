# Generated by Django 3.2.8 on 2022-01-12 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0012_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='47B5DCAD12', editable=False, max_length=10, unique=True),
        ),
    ]
