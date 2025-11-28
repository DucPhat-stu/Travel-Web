"""
Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('django-admin/', admin.site.urls),
    
    # Core pages (Homepage, About, Contact)
    path('', include('core.urls')),
    
    # Authentication
    path('users/', include('users.urls')),
    
    # Services (uncomment khi đã tạo)
    # path('tours/', include('tours.urls')),
    # path('hotels/', include('hotels.urls')),
    # path('flight/', include('flight.urls')),
    # path('booking/', include('bookings.urls')),
    # path('chatbot/', include('chatbot.urls')),
    path('admin-panel/', include('admin_panel.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)