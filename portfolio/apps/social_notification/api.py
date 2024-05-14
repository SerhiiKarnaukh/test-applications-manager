from django.http import JsonResponse

from rest_framework.decorators import api_view

from .models import Notification
from .serializers import NotificationSerializer
from social_profiles.models import Profile


@api_view(['GET'])
def notifications(request):
    request_user = Profile.objects.get(user=request.user)

    received_notifications = request_user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notifications, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def read_notification(request, pk):
    request_user = Profile.objects.get(user=request.user)

    notification = Notification.objects.filter(created_for=request_user).get(pk=pk)
    notification.is_read = True
    notification.save()

    return JsonResponse({'message': 'notification read'})
