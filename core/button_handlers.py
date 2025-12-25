"""
File xử lý logic cho các nút trong giao diện web
Tập trung tất cả các URL routing và logic điều hướng
"""

from django.urls import reverse
from django.http import JsonResponse

# Mapping các nút với URL tương ứng
BUTTON_ACTIONS = {
    # Navigation buttons
    'home': 'core:home',
    'about': 'core:about',
    'destinations': 'core:destinations',
    'destination_details': 'core:destinations',
    'tours': 'tours:tour_list',
    'tour_details': 'tours:tour_list',
    'gallery': 'core:gallery',
    'blog': 'core:blog',
    'blog_details': 'core:blog',
    'testimonials': 'core:testimonials',
    'faq': 'core:faq',
    'terms': 'core:terms',
    'privacy': 'core:privacy',
    'contact': 'core:contact',
    
    # Service buttons
    'booking': 'bookings:booking_list',
    'flight': 'flight:flight_list',
    'chatbot': 'chatbot:chatbot',
    
    # Authentication buttons
    'login': 'users:login',
    'logout': 'users:logout',
    'register': 'users:register',
    'edit_profile': 'users:edit_profile',
    
    # Action buttons
    'book_now': 'bookings:booking_list',
    'view_details': 'tours:tour_list',
    'view_tour': 'tours:tour_list',
    'view_all_tours': 'tours:tour_list',
    'contact_expert': 'core:contact',
    'get_quote': 'core:contact',
    'start_exploring': 'tours:tour_list',
    'browse_tours': 'tours:tour_list',
}

def get_button_url(button_name, **kwargs):
    """
    Lấy URL cho một nút dựa trên tên của nó
    
    Args:
        button_name: Tên của nút (key trong BUTTON_ACTIONS)
        **kwargs: Các tham số bổ sung cho URL (ví dụ: tour_id)
    
    Returns:
        URL string hoặc None nếu không tìm thấy
    """
    url_name = BUTTON_ACTIONS.get(button_name)
    if url_name:
        try:
            return reverse(url_name, kwargs=kwargs if kwargs else None)
        except Exception as e:
            print(f"Error generating URL for {button_name}: {e}")
            return None
    return None

def get_all_button_urls():
    """
    Lấy tất cả các URL cho các nút
    Hữu ích cho việc render template
    """
    urls = {}
    for button_name in BUTTON_ACTIONS.keys():
        urls[button_name] = get_button_url(button_name)
    return urls

# Context processor để cung cấp button URLs cho tất cả templates
def button_urls_context(request):
    """
    Context processor để thêm button URLs vào context của tất cả templates
    Thêm vào TEMPLATES['OPTIONS']['context_processors'] trong settings.py
    """
    return {
        'button_urls': get_all_button_urls(),
        'get_button_url': get_button_url,
    }

# Các hàm xử lý logic cho các nút đặc biệt
def handle_book_tour(request, tour_id):
    """Xử lý khi người dùng click nút 'Book Now' trên tour"""
    from tours.models import Tour
    try:
        tour = Tour.objects.get(tour_id=tour_id)
        return {
            'success': True,
            'redirect_url': reverse('bookings:booking_list'),
            'message': f'Redirecting to booking for {tour.name}'
        }
    except Tour.DoesNotExist:
        return {
            'success': False,
            'message': 'Tour not found'
        }

def handle_book_flight(request, flight_id):
    """Xử lý khi người dùng click nút 'Book Now' trên flight"""
    from flight.models import Flight
    try:
        flight = Flight.objects.get(flight_id=flight_id)
        return {
            'success': True,
            'redirect_url': reverse('bookings:booking_list'),
            'message': f'Redirecting to booking for {flight.airline}'
        }
    except Flight.DoesNotExist:
        return {
            'success': False,
            'message': 'Flight not found'
        }

def handle_contact_expert(request):
    """Xử lý khi người dùng click nút 'Contact Expert'"""
    return {
        'success': True,
        'redirect_url': reverse('core:contact'),
        'message': 'Redirecting to contact page'
    }

def handle_get_quote(request):
    """Xử lý khi người dùng click nút 'Get Quote'"""
    return {
        'success': True,
        'redirect_url': reverse('core:contact'),
        'message': 'Redirecting to quote page'
    }

# API endpoint để xử lý button clicks
def button_click_handler(request):
    """
    API endpoint để xử lý button clicks
    POST request với button_name và optional parameters
    """
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            button_name = data.get('button_name')
            params = data.get('params', {})
            
            # Lấy URL cho nút
            url = get_button_url(button_name, **params)
            
            if url:
                return JsonResponse({
                    'success': True,
                    'redirect_url': url,
                    'message': f'Button {button_name} clicked'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'Unknown button: {button_name}'
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Only POST requests are allowed'
    }, status=405)
