from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.urls import reverse
from urllib.parse import quote

from users.middleware import AdminRequiredMixin
from users.models import User
from bookings.models import Booking
from tours.models import Tour
from hotels.models import Hotel
from flight.models import Flight
from catalog.models import Destination, Package
from users.services import SessionService
from django.db.models import Avg
from datetime import timedelta
from django.utils import timezone

def is_admin(user):
    # Kiểm tra cả Django's built-in auth và custom session auth
    if hasattr(user, 'is_authenticated') and user.is_authenticated:
        return user.is_admin()
    # Nếu không có user object, kiểm tra từ request (sẽ được xử lý trong decorator)
    return False

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = "admin_panel/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "total_users": User.objects.count(),
                "total_admins": User.objects.filter(role="admin").count(),
                "total_bookings": Booking.objects.count(),
                "total_tours": Tour.objects.count(),
                "total_hotels": Hotel.objects.count(),
                "total_flights": Flight.objects.count(),
                "total_destinations": Destination.objects.count(),
                "total_packages": Package.objects.count(),
                "recent_users": User.objects.order_by('-created_at')[:10],  # Get 10 most recent users
            }
        )
        return ctx

def admin_required_custom(view_func):
    """
    Custom decorator để kiểm tra admin dựa trên session thay vì Django's auth
    """
    from functools import wraps

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Kiểm tra session authentication
        if not SessionService.is_authenticated(request):
            from django.contrib import messages
            messages.warning(request, 'Vui lòng đăng nhập để tiếp tục!')
            login_url = reverse('users:login')
            next_url = quote(request.get_full_path(), safe='/')
            return redirect(f'{login_url}?next={next_url}')

        # Kiểm tra quyền admin
        if not SessionService.is_admin(request):
            from django.contrib import messages
            messages.error(request, 'Bạn không có quyền truy cập trang này!')
            return redirect('core:home')

        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required_custom
def dashboard(request):
    tours_count = Tour.objects.count()
    hotels_count = Hotel.objects.count()
    flights_count = Flight.objects.count()
    bookings_count = Booking.objects.count()
    users_count = User.objects.count()

    context = {
        'tours_count': tours_count,
        'hotels_count': hotels_count,
        'flights_count': flights_count,
        'bookings_count': bookings_count,
        'users_count': users_count,
    }
    return render(request, 'admin-dashboard.html', context)

@admin_required_custom
def manage_tours(request):
    tours = Tour.objects.all()
    return render(request, 'admin-tour.html', {'tours': tours})

@admin_required_custom
def manage_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'admin-booking.html', {'bookings': bookings})

@admin_required_custom
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin-user.html', {'users': users})

@admin_required_custom
def database_stats(request):
    # Render the admin HTML view. For API usage, use `database_stats_api` below.
    total_users = User.objects.count()
    admin_users = User.objects.filter(role='admin').count()
    active_users = User.objects.filter(is_active=True).count()

    total_bookings = Booking.objects.count()
    tour_bookings = Booking.objects.filter(booking_type='tour').count()
    hotel_bookings = Booking.objects.filter(booking_type='hotel').count()
    flight_bookings = Booking.objects.filter(booking_type='flight').count()

    total_tours = Tour.objects.count()
    active_tours = Tour.objects.filter(is_active=True).count()
    tour_price_avg = Tour.objects.aggregate(avg=Avg('price'))['avg'] or 0

    total_hotels = Hotel.objects.count()
    active_hotels = Hotel.objects.filter(is_active=True).count()
    total_flights = Flight.objects.count()
    active_flights = Flight.objects.filter(is_active=True).count()

    total_destinations = Destination.objects.count()
    total_packages = Package.objects.count()

    # Recent data
    recent_users = User.objects.order_by('-created_at')[:10]
    recent_bookings = Booking.objects.order_by('-created_at')[:10]

    # New users in last 30 days
    since = timezone.now() - timedelta(days=30)
    recent_user_registrations = User.objects.filter(created_at__gte=since).count()

    context = {
        'total_users': total_users,
        'admin_users': admin_users,
        'active_users': active_users,
        'recent_user_registrations': recent_user_registrations,
        'total_bookings': total_bookings,
        'tour_bookings': tour_bookings,
        'hotel_bookings': hotel_bookings,
        'flight_bookings': flight_bookings,
        'total_tours': total_tours,
        'active_tours': active_tours,
        'tour_price_avg': tour_price_avg,
        'total_hotels': total_hotels,
        'active_hotels': active_hotels,
        'total_flights': total_flights,
        'active_flights': active_flights,
        'total_destinations': total_destinations,
        'total_packages': total_packages,
        'recent_users': recent_users,
        'recent_bookings': recent_bookings,
    }

    return render(request, 'admin_panel/database_stats.html', context)


@admin_required_custom
def database_stats_api(request):
    # JSON API for programmatic access
    stats = {
        'total_users': User.objects.count(),
        'total_admins': User.objects.filter(role='admin').count(),
        'total_bookings': Booking.objects.count(),
        'total_tours': Tour.objects.count(),
        'total_hotels': Hotel.objects.count(),
        'total_flights': Flight.objects.count(),
        'total_destinations': Destination.objects.count(),
        'total_packages': Package.objects.count(),
    }
    return JsonResponse(stats)
