from django.http import JsonResponse

from rest_framework.decorators import api_view

from social_profiles.models import Profile

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer


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
    conversation = Conversation.objects.filter(
        users__in=list([request_user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation,
                                              context={'request': request})

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_get_or_create(request, slug):

    user = Profile.objects.get(slug=slug)
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

    return JsonResponse(serializer.data, safe=False)
