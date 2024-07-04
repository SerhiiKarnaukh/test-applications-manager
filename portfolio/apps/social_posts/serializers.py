from rest_framework import serializers

from social_profiles.serializers import ProfileSerializer

from .models import Post, PostAttachment, Comment, Trend


class PostAttachmentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PostAttachment
        fields = ('id', 'image_url',)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request is not None and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class PostSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'body',
            'is_private',
            'likes_count',
            'comments_count',
            'created_by',
            'created_at_formatted',
            'attachments',
        )


class CommentSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'created_by',
            'created_at_formatted',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'body',
            'likes_count',
            'comments_count',
            'created_by',
            'created_at_formatted',
            'comments',
            'attachments',
        )


class TrendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trend
        fields = (
            'id',
            'hashtag',
            'occurences',
        )
