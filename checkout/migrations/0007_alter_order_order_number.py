# Generated by Django 3.2.8 on 2021-12-09 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='AE344CADAF', editable=False, max_length=10, unique=True),
        ),
    ]
