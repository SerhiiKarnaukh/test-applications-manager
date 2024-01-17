from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics

from .forms import ProfileForm
from .models import Profile, FriendshipRequest

from .serializers import ProfileSerializer, FriendshipRequestSerializer, SocialProfileCreateSerializer


class SocialProfileCreateView(generics.CreateAPIView):
    serializer_class = SocialProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_instance = serializer.save()
        account_instance.is_active = True
        account_instance.save()

        Profile.objects.create(user=account_instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
def me(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, context={'request': request})
        response_data = serializer.data
        return Response(response_data)
    except Profile.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={'message': 'Profile does not exist for this user'})


@api_view(['GET'])
def friends(request, slug):
    user = Profile.objects.get(slug=slug)
    request_user = Profile.objects.get(user=request.user)
    requests = []

    if user == request_user:
        requests = FriendshipRequest.objects.filter(
            created_for=request_user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests,
                                               context={'request': request},
                                               many=True)
        requests = requests.data

    friends = user.friends.all()

    return JsonResponse(
        {
            'user':
            ProfileSerializer(user, context={
                'request': request
            }).data,
            'friends':
            ProfileSerializer(friends, context={
                'request': request
            }, many=True).data,
            'requests':
            requests
        },
        safe=False)


@api_view(['POST'])
def send_friendship_request(request, slug):
    user = Profile.objects.get(slug=slug)
    request_user = Profile.objects.get(user=request.user)

    check1 = FriendshipRequest.objects.filter(created_for=request_user).filter(
        created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(
        created_by=request_user)

    if not check1 and not check2:
        FriendshipRequest.objects.create(created_for=user,
                                         created_by=request_user)

        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})


@api_view(['POST'])
def handle_request(request, slug, status):
    user = Profile.objects.get(slug=slug)
    request_user = Profile.objects.get(user=request.user)
    friendship_request = FriendshipRequest.objects.filter(
        created_for=request_user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request_user)
    user.friends_count = user.friends_count + 1
    user.save()
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    return JsonResponse({'message': 'friendship request updated'})


@api_view(['POST'])
def editprofile(request):
    user = request.user
    email = request.data.get('email')
    username = request.data.get('username')

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if Profile.objects.exclude(id=profile.id).filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists!'})
    elif Profile.objects.exclude(id=profile.id).filter(
            username=username).exists():
        return JsonResponse({'message': 'Username already exists!'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_profile = form.save()
            new_avatar_url = None
            if new_profile.avatar:
                new_avatar_url = request.build_absolute_uri(
                    new_profile.avatar.url)
            return JsonResponse({
                'message': 'Information updated successfully',
                'new_slug': new_profile.slug,
                'new_avatar': new_avatar_url,
            })

        return JsonResponse({'message': 'Invalid form data!'})
