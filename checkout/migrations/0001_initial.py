# Generated by Django 3.2.8 on 2021-12-05 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('user_profile', '0002_discount_offer_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(default='FBF93039CC', editable=False, max_length=10, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('discount_percentage', models.PositiveIntegerField(default=0, null=True)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cardholder_full_name', models.CharField(max_length=32)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='user_profile.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_price', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.order')),
            ],
        ),
    ]
