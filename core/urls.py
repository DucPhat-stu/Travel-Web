from django.urls import path
from . import views
from .button_handlers import button_click_handler

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('newsletter/submit/', views.newsletter_submit, name='newsletter_submit'),
    path('gallery/', views.gallery, name='gallery'),
    path('destinations/', views.destinations, name='destinations'),
    path('destinations/destination-details.html', views.destination_detail, name='destination_detail'),
    path('blog/', views.blog, name='blog'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faq/', views.faq, name='faq'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    
    # API endpoint cho button handlers
    path('api/button-click/', button_click_handler, name='button_click'),
]