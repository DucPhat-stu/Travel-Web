from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import ChatMessage
from .serializers import ChatMessageSerializer
from users.permissions import IsAdminOrReadOnly


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
