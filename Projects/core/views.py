from django.shortcuts import render

# View trang chủ
def home(request):
    return render(request, "core/home.html")

# View trang giới thiệu
def about(request):
    return render(request, "core/about.html")

# View trang liên hệ
def contact_view(request):
    """Render contact page with static context data."""
    context = {
        "support_email": "support@travel-tourism.com",
        "support_phone": "+84 123 456 789",
    }
    return render(request, "core/contact.html", context)