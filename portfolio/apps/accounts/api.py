from rest_framework.response import Response
from rest_framework import status
from social_profiles.models import Profile
from social_profiles.serializers import ProfileSerializer

from rest_framework.decorators import api_view


@api_view(['GET'])
def me(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        response_data = serializer.data
        response_data.update({
            'username': user.username,
        })
        return Response(response_data)
    except Profile.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={'message': 'Profile does not exist for this user'})
