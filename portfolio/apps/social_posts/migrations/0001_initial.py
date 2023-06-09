# Generated by Django 4.1.7 on 2023-05-02 15:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('social_profiles', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='social/posts', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_attachments', to='social_profiles.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attachments', models.ManyToManyField(blank=True, to='social_posts.postattachment')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='social_profiles.profile')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
