# Generated by Django 4.1.7 on 2023-05-22 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_posts', '0003_post_comments_count_comment_post_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=255)),
                ('occurences', models.IntegerField()),
            ],
        ),
    ]
