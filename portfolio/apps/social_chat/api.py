from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from social_profiles.models import Profile
from .models import Conversation, ConversationMessage

from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer

from social_notification.utils import create_notification


@api_view(['GET'])
def conversation_list(request):
    request_user = Profile.objects.get(user=request.user)
    conversations = Conversation.objects.filter(users__in=list([request_user]))
    serializer = ConversationSerializer(conversations,
                                        context={'request': request},
                                        many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_detail(request, pk):
    request_user = Profile.objects.get(user=request.user)
    try:
        conversation = Conversation.objects.filter(
            users__in=[request_user]
        ).get(pk=pk)
    except Conversation.DoesNotExist:
        raise NotFound("Conversation not found.")

    serializer = ConversationDetailSerializer(conversation,
                                              context={'request': request})

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_get_or_create(request, slug):

    user = get_object_or_404(Profile, slug=slug)
    request_user = Profile.objects.get(user=request.user)

    conversations = Conversation.objects.filter(
        users__in=list([request_user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request_user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation,
                                              context={'request': request})

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def conversation_send_message(request, pk):
    request_user = Profile.objects.get(user=request.user)
    conversation = Conversation.objects.filter(
        users__in=list([request_user])).get(pk=pk)

    for user in conversation.users.all():
        if user != request_user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request_user,
        sent_to=sent_to)

    serializer = ConversationMessageSerializer(conversation_message,
                                               context={'request': request})

    create_notification(request, 'chat_message', conversation_message_id=conversation_message.id)

    # send websocket message
    channel_layer = get_channel_layer()
    group_name = f'social_chat_{conversation.id}'
    async_to_sync(channel_layer.group_send)(group_name, {
        'type': 'send_message',
        'message': serializer.data
    })

    return JsonResponse(serializer.data, safe=False)
