from django.http import JsonResponse

from rest_framework.decorators import api_view


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
    })
