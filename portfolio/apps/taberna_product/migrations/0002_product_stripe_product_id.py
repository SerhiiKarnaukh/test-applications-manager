# Generated by Django 5.1.5 on 2025-02-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taberna_product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
