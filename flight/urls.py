from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

app_name = 'flight'

router = DefaultRouter()
router.register(r'flights', api.FlightViewSet, basename='flight')

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('api/', include(router.urls)),
]
