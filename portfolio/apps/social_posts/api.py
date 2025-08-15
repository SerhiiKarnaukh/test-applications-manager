from django.http import JsonResponse
from django.db.models import Q
import os

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from social_notification.utils import create_notification
from .forms import PostForm, AttachmentForm

from .models import Post, Like, Comment, Trend
from social_profiles.models import Profile, FriendshipRequest

from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer, TrendSerializer
from social_profiles.serializers import ProfileSerializer

from .pagination import PostPagination
from .utils import get_trending_posts, get_user_feed_posts


@api_view(['GET'])
def post_list(request):
    trend = request.GET.get('trend', '').lower()

    if trend:
        posts = get_trending_posts(trend)
    else:
        posts = get_user_feed_posts(request.user)

    paginator = PostPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    posts_serializer = PostSerializer(paginated_posts, context={'request': request}, many=True)

    return paginator.get_paginated_response({
        'posts': posts_serializer.data
    })


@api_view(['GET'])
def post_detail(request, pk):
    request_user = None
    user_ids = []
    if request.user.is_authenticated:
        request_user = Profile.objects.get(user=request.user)

    if request_user is not None:
        user_ids.append(request_user.id)
        for user in request_user.friends.all():
            user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)

    return Response({
        'post': PostDetailSerializer(post, context={'request': request}).data
    })


@api_view(['GET'])
def post_list_profile(request, slug):
    profile = Profile.objects.get(slug=slug)
    request_user = None
    if request.user.is_authenticated:
        request_user = Profile.objects.get(user=request.user)
    created_by_id = profile.id
    posts = Post.objects.filter(created_by_id=created_by_id)

    if request_user is not None:
        if request_user not in profile.friends.all() and request_user.id != profile.id:
            posts = posts.filter(is_private=False)

        can_send_friendship_request = True
        if request_user in profile.friends.all():
            can_send_friendship_request = False

        check1 = FriendshipRequest.objects.filter(created_for=request_user).filter(created_by=profile)
        check2 = FriendshipRequest.objects.filter(created_for=profile).filter(created_by=request_user)

        if check1.exists() or check2.exists():
            can_send_friendship_request = False
            if check1.exists() and check1.first().status == 'rejected':
                can_send_friendship_request = 'rejected'
            if check2.exists() and check2.first().status == 'rejected':
                can_send_friendship_request = 'rejected'
    else:
        can_send_friendship_request = False
        posts = posts.filter(is_private=False)

    paginator = PostPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    posts_serializer = PostSerializer(paginated_posts, context={'request': request}, many=True)

    profile_serializer = ProfileSerializer(profile,
                                           context={'request': request})

    return paginator.get_paginated_response({
        'posts': posts_serializer.data,
        'profile': profile_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    })


@api_view(['POST'])
def post_create(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    form = PostForm(request.POST)
    user = request.user
    profile = Profile.objects.get(user=user)

    images = [
        value for key, value in request.FILES.items()
        if key.startswith('images')
    ]

    attachments = []

    for image in images:
        attachment_form = AttachmentForm(data=None, files={'image': image})
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.created_by = profile
            attachment.save()
            attachments.append(attachment)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = profile
        post.save()

        if attachments:
            for attachment in attachments:
                post.attachments.add(attachment)

        profile.posts_count = profile.posts_count + 1
        profile.save()

        serializer = PostSerializer(post, context={'request': request})

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Form is not valid'}, status=400)


@api_view(['GET', 'POST'])
def search(request):
    query = request.data.get('query') if request.method == 'POST' else request.query_params.get('query')
    request_user = None
    user_ids = []
    if request.user.is_authenticated:
        request_user = Profile.objects.get(user=request.user)

    profiles = Profile.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query))
    profile_serializer = ProfileSerializer(profiles,
                                           context={'request': request},
                                           many=True)

    if request_user is not None:
        user_ids.append(request_user.id)
        for user in request_user.friends.all():
            user_ids.append(user.id)

    posts = Post.objects.filter(
        Q(body__icontains=query, is_private=False) |
        Q(created_by_id__in=list(user_ids), body__icontains=query)
    )
    paginator = PostPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    posts_serializer = PostSerializer(paginated_posts, context={'request': request}, many=True)

    return paginator.get_paginated_response({
        'profiles': profile_serializer.data,
        'posts': posts_serializer.data
    })


@api_view(['POST'])
def post_like(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    post = Post.objects.get(pk=pk)
    request_user = Profile.objects.get(user=request.user)

    if not post.likes.filter(created_by=request_user):
        like = Like.objects.create(created_by=request_user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        if post.created_by != request_user:
            create_notification(request, 'post_like', post_id=post.id)

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})


@api_view(['POST'])
def post_create_comment(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    request_user = Profile.objects.get(user=request.user)
    comment = Comment.objects.create(body=request.data.get('body'),
                                     created_by=request_user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment, context={'request': request})

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    request_user = Profile.objects.get(user=request.user)

    try:
        post = Post.objects.filter(created_by=request_user).get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'detail': 'Not found.'}, status=404)

    for attachment in post.attachments.all():
        if attachment.image:
            if os.path.isfile(attachment.image.path):
                os.remove(attachment.image.path)
        attachment.delete()
    post.delete()

    request_user.posts_count = request_user.posts_count - 1
    request_user.save()

    return JsonResponse({'message': 'post deleted'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_report(request, pk):
    request_user = Profile.objects.get(user=request.user)
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request_user)
    post.save()

    return JsonResponse({'message': 'post reported'})
