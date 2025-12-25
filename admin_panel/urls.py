from django.urls import path
from .views import AdminDashboardView, dashboard, manage_tours, manage_bookings, manage_users, database_stats, database_stats_api


app_name = 'admin_panel'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('dashboard/', dashboard, name='admin_dashboard'),
    path('tours/', manage_tours, name='manage_tours'),
    path('bookings/', manage_bookings, name='manage_bookings'),
    path('users/', manage_users, name='manage_users'),
    path('database-stats/', database_stats, name='database_stats'),
    path('database-stats/data/', database_stats_api, name='database_stats_api'),
]

