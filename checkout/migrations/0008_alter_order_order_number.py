# Generated by Django 3.2.8 on 2022-01-10 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='D9AEFD7498', editable=False, max_length=10, unique=True),
        ),
    ]
