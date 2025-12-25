from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tour
from bookings.models import Booking
from bookings.services import BookingService

def tour_list(request):
    tours = Tour.objects.filter(is_active=True)
    return render(request, 'tours.html', {'tours': tours})

def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, tour_id=tour_id, is_active=True)
    related_tours = Tour.objects.filter(location=tour.location, is_active=True).exclude(tour_id=tour_id)[:4]

    # Automatically create preview data for the tour
    preview_data = {
        'tour_id': tour_id,
        'tour_name': tour.name,
        'destination_name': tour.location,
        'package_id': None,
        'package_name': None,
        'number_of_people': 1,
        'total_cost': float(tour.price),
        'passenger_name': request.user.get_full_name() or request.user.username if request.user.is_authenticated else '',
        'email': request.user.email if request.user.is_authenticated else '',
        'flight_details': f"Tour: {tour.name}\nĐiểm đến: {tour.location}",
    }

    # Save to session
    request.session['ticket_preview'] = preview_data

    return render(request, 'tour-details.html', {'tour': tour, 'related_tours': related_tours})

def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, tour_id=tour_id, is_active=True)

    # If GET request, redirect to tour detail page
    if request.method == 'GET':
        return redirect('tours:tour_detail', tour_id=tour_id)

    # For POST requests, require authentication
    if not request.user.is_authenticated:
        from django.urls import reverse
        login_url = reverse('users:login')
        next_url = reverse('tours:tour_detail', args=[tour_id])
        return redirect(f'{login_url}?next={next_url}')

    if request.method == 'POST':
        number_of_people = int(request.POST.get('travelers', 1))
        booking_date_str = request.POST.get('date')

        # Parse booking date
        from datetime import datetime
        try:
            booking_date = datetime.strptime(booking_date_str, '%B %d-%d, %Y').date()
        except (ValueError, TypeError):
            booking_date = None

        # Create booking for individual tour
        booking = BookingService.create_booking(
            user=request.user,
            booking_type='tour',
            number_of_people=number_of_people,
            total_price=tour.price * number_of_people,
            tour=tour,
            booking_date=booking_date
        )

        # Create ticket preview in session for payment
        preview_data = {
            'tour_id': tour_id,
            'tour_name': tour.name,
            'destination_name': tour.location,
            'number_of_people': number_of_people,
            'total_cost': float(booking.total_price),
            'passenger_name': request.user.get_full_name() or request.user.username,
            'booking_date': booking_date_str,
        }

        request.session['ticket_preview'] = preview_data
        messages.success(request, 'Đã tạo yêu cầu đặt tour. Vui lòng thanh toán để hoàn tất.')
        return redirect('bookings:ticket_detail', ticket_id='preview')

    return redirect('tours:tour_detail', tour_id=tour_id)
