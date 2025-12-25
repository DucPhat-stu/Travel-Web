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
    
    # Services
    path('tours/', include('tours.urls')),
    path('hotels/', include('hotels.urls')),
    path('flight/', include('flight.urls')),
    path('bookings/', include('bookings.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('captcha/', include('captcha.urls')),

    # API
    path('api/', include(('travel_tourism.api_urls', 'api'), namespace='api')),
]

# Serve static and media files in development
if settings.DEBUG:
    # Serve static files from STATICFILES_DIRS
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve assets folder directly for templates using relative paths
    assets_path = settings.BASE_DIR / 'assets'
    if assets_path.exists():
        urlpatterns += static('/assets/', document_root=assets_path)