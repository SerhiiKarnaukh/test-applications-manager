# Generated by Django 5.0 on 2024-01-17 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='registration_source',
        ),
    ]
