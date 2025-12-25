from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Booking list & search
    path('', views.booking_list, name='booking_list'),

    # Contact booking form
    path('contact/<int:package_id>/', views.contact_booking, name='contact_booking'),

    # Booking details & payment
    path('details/', views.booking_details, name='booking_details'),

    # Confirm payment
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),

    # Ticket detail
    path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    # Create ticket from tour
    path('create-ticket-from-tour/', views.create_ticket_from_tour, name='create_ticket_from_tour'),

    # Payment
    path('payment/<str:ticket_id>/', views.payment, name='payment'),

    # Booking confirm (old)
    path('confirm/', views.booking_confirm, name='booking_confirm'),

    # Booking detail (old)
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),

    # Booking history
    path('history/', views.booking_history, name='booking_history'),

    # Cancel booking
    path('<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),

    # API endpoints
    path('api/recommendations/', views.booking_api_recommendations, name='api_recommendations'),
]
