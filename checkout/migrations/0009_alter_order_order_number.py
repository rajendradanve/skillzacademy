# Generated by Django 3.2.8 on 2022-01-12 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='43FB4A83C4', editable=False, max_length=10, unique=True),
        ),
    ]
