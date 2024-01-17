from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from .models import Profile, FriendshipRequest


class SocialProfileCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = ('id', 'email', 'username', 'password',  'first_name', 'last_name',)

    def create(self, validated_data):
        user = super().create(validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):

    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)

    def get_full_name(self, obj):
        return obj.full_name()

    class Meta:
        model = Profile
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'slug',
            'avatar_url',
            'friends_count',
            'posts_count',
            'full_name',
        )


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = (
            'id',
            'created_by',
        )
