# Generated by Django 5.0 on 2023-12-18 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_registration_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
