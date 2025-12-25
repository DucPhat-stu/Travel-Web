from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .button_handlers import get_all_button_urls

# View trang chủ
def home(request):
    context = {
        'button_urls': get_all_button_urls(),
    }
    return render(request, "index.html", context)

# View trang giới thiệu
def about(request):
    return render(request, "about.html")

# View trang liên hệ
def contact_view(request):
    """Render contact page with static context data."""
    context = {
        "support_email": "support@travel-tourism.com",
        "support_phone": "+84 123 456 789",
    }
    return render(request, "contact.html", context)

@require_http_methods(["POST"])
def contact_submit(request):
    """Handle contact form submission."""
    try:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate form data
        if not all([name, email, subject, message]):
            return HttpResponse('Vui lòng điền đầy đủ tất cả các trường.', status=400)
        
        # TODO: Send email or save to database
        # For now, return OK for success
        # You can add email sending logic here
        
        return HttpResponse('OK')
        
    except Exception as e:
        return HttpResponse(f'Lỗi khi gửi tin nhắn: {str(e)}', status=500)

@require_http_methods(["POST"])
def newsletter_submit(request):
    """Handle newsletter subscription."""
    try:
        email = request.POST.get('email', '').strip()
        
        # Validate email
        if not email:
            return HttpResponse('Vui lòng nhập địa chỉ email.', status=400)
        
        # TODO: Save to database or email service
        # For now, return OK for success
        
        return HttpResponse('OK')
        
    except Exception as e:
        return HttpResponse(f'Lỗi khi đăng ký: {str(e)}', status=500)

# View trang gallery
def gallery(request):
    return render(request, "gallery.html")

# View trang destinations
def destinations(request):
    return render(request, "destinations.html")

# View trang destination details (static template)
def destination_detail(request):
    return render(request, "destination-details.html")

# View trang blog
def blog(request):
    return render(request, "blog.html")

# View trang testimonials
def testimonials(request):
    return render(request, "testimonials.html")

# View trang FAQ
def faq(request):
    return render(request, "faq.html")

# View trang Terms
def terms(request):
    return render(request, "terms.html")

# View trang Privacy
def privacy(request):
    return render(request, "privacy.html")