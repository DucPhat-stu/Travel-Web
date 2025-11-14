from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('django-admin/', admin.site.urls),
    
    # App URLs
    path('', include('core.urls')),  # Homepage và các trang chung
    path('users/', include('users.urls')),  # Auth: register, login, logout...
    path('tours/', include('tours.urls')),  # Quản lý tours
    path('hotels/', include('hotels.urls')),  # Quản lý hotels
    path('flight/', include('flight.urls')),  # Quản lý flights
    path('booking/', include('bookings.urls')),  # Quản lý bookings
    path('chatbot/', include('chatbot.urls')),  # Chatbot
    path('admin-panel/', include('admin_panel.urls')),  # Admin dashboard
]

# Serve static files trong development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)