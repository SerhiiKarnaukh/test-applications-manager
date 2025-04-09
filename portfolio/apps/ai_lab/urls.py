from django.urls import path

from . import api

app_name = 'ai_lab'

urlpatterns = [
    path('', api.AiLabChatView.as_view(), name='ai_lab_api'),
    path('image-generator/', api.AiLabImageGeneratorView.as_view(), name='ai_lab_image_generator'),
]
