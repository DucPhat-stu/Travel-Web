from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Tour
from .serializers import TourSerializer
from users.permissions import IsAdminOrReadOnly


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.filter(is_active=True)
    serializer_class = TourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
