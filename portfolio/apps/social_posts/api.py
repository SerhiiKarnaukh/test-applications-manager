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
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request, slug):
    profile = Profile.objects.get(slug=slug)
    created_by_id = profile.id
    posts = Post.objects.filter(created_by_id=created_by_id)

    posts_serializer = PostSerializer(posts, many=True)
    profile_serializer = ProfileSerializer(profile)

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
    profile_serializer = ProfileSerializer(profiles, many=True)

    posts = Post.objects.filter(body__icontains=query)
    posts_serializer = PostSerializer(posts, many=True)

    return JsonResponse(
        {
            'profiles': profile_serializer.data,
            'posts': posts_serializer.data
        },
        safe=False)
