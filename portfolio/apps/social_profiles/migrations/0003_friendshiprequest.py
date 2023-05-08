# Generated by Django 4.1.7 on 2023-05-05 14:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('social_profiles', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendshipRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='sent', max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_friendshiprequests', to='social_profiles.profile')),
                ('created_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_friendshiprequests', to='social_profiles.profile')),
            ],
        ),
    ]
