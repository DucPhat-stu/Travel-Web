from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

app_name = 'chatbot'

router = DefaultRouter()
router.register(r'chat-messages', api.ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('api/', include(router.urls)),
]
