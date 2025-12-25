from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

app_name = 'tours'

router = DefaultRouter()
router.register(r'tours', api.TourViewSet, basename='tour')

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('<int:tour_id>/book/', views.book_tour, name='book_tour'),
    path('api/', include(router.urls)),
]
