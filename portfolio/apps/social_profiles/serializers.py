from rest_framework import serializers

from .models import Profile, FriendshipRequest


class ProfileSerializer(serializers.ModelSerializer):

    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)

    class Meta:
        model = Profile
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'slug',
            'avatar_url',
            'friends_count',
        )


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = (
            'id',
            'created_by',
        )
