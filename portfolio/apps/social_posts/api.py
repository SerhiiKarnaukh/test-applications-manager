from django.http import JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view

from social_notification.utils import create_notification
from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend

from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer, TrendSerializer

from social_profiles.serializers import ProfileSerializer
from social_profiles.models import Profile, FriendshipRequest


@api_view(['GET'])
def post_list(request):
    request_user = None
    if request.user.is_authenticated:
        request_user = Profile.objects.get(user=request.user)

    posts = Post.objects.all()

    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains='#' + trend)

    posts_serializer = PostSerializer(posts,
                                      context={'request': request},
                                      many=True)
    user_ids = []
    if request_user is not None:
        user_ids = [request_user.id]
        for user in request_user.friends.all():
            user_ids.append(user.id)
    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    friends_posts = PostSerializer(posts,
                                   context={'request': request},
                                   many=True)

    return JsonResponse(
        {
            'posts': posts_serializer.data,
            'friends_posts': friends_posts.data
        },
        safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    return JsonResponse({
        'post':
        PostDetailSerializer(post, context={
            'request': request
        }).data
    })


@api_view(['GET'])
def post_list_profile(request, slug):
    profile = Profile.objects.get(slug=slug)
    request_user = Profile.objects.get(user=request.user)
    created_by_id = profile.id
    posts = Post.objects.filter(created_by_id=created_by_id)

    posts_serializer = PostSerializer(posts,
                                      context={'request': request},
                                      many=True)
    profile_serializer = ProfileSerializer(profile,
                                           context={'request': request})

    can_send_friendship_request = True

    if request_user in profile.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for=request_user).filter(created_by=profile)
    check2 = FriendshipRequest.objects.filter(created_for=profile).filter(created_by=request_user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse(
        {
            'posts': posts_serializer.data,
            'profile': profile_serializer.data,
            'can_send_friendship_request': can_send_friendship_request
        },
        safe=False)


@api_view(['POST'])
def post_create(request):
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
        return JsonResponse({'error': 'add something here later!...'})


@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']

    profiles = Profile.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query))
    profile_serializer = ProfileSerializer(profiles,
                                           context={'request': request},
                                           many=True)

    posts = Post.objects.filter(body__icontains=query)
    posts_serializer = PostSerializer(posts,
                                      context={'request': request},
                                      many=True)

    return JsonResponse(
        {
            'profiles': profile_serializer.data,
            'posts': posts_serializer.data
        },
        safe=False)


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    request_user = Profile.objects.get(user=request.user)

    if not post.likes.filter(created_by=request_user):
        like = Like.objects.create(created_by=request_user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        create_notification(request, 'post_like', post_id=post.id)

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})


@api_view(['POST'])
def post_create_comment(request, pk):
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
