from rest_framework import serializers

from social_profiles.serializers import ProfileSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'body',
            'likes_count',
            'created_by',
            'created_at_formatted',
        )
