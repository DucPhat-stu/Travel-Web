from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

app_name = 'hotels'

router = DefaultRouter()
router.register(r'hotels', api.HotelViewSet, basename='hotel')

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('api/', include(router.urls)),
]
