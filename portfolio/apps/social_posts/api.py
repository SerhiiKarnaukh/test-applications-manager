from django.http import JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer
from social_profiles.serializers import ProfileSerializer
from social_profiles.models import Profile


@api_view(['GET'])
def post_list(request):
    request_user = None
    if request.user.is_authenticated:
        request_user = Profile.objects.get(user=request.user)

    posts = Post.objects.all()
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
def post_list_profile(request, slug):
    profile = Profile.objects.get(slug=slug)
    created_by_id = profile.id
    posts = Post.objects.filter(created_by_id=created_by_id)

    posts_serializer = PostSerializer(posts,
                                      context={'request': request},
                                      many=True)
    profile_serializer = ProfileSerializer(profile,
                                           context={'request': request})

    return JsonResponse(
        {
            'posts': posts_serializer.data,
            'profile': profile_serializer.data
        },
        safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)
    user = request.user
    profile = Profile.objects.get(user=user)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = profile
        post.save()

        serializer = PostSerializer(post)

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
