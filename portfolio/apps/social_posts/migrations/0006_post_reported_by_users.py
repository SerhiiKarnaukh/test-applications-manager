# Generated by Django 5.0.6 on 2024-07-08 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_posts', '0005_post_is_private'),
        ('social_profiles', '0013_profile_people_you_may_know'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reported_by_users',
            field=models.ManyToManyField(blank=True, to='social_profiles.profile'),
        ),
    ]