# Generated by Django 3.2.8 on 2022-01-14 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0020_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='7A77F6A0E5', editable=False, max_length=10, unique=True),
        ),
    ]