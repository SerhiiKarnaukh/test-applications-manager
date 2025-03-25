from django.urls import path

from . import api

app_name = 'ai_lab'

urlpatterns = [
    path('', api.AiLabTestView.as_view(), name='ai_lab_api'),
]
