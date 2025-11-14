from django.shortcuts import render

def home_view(request):
    """
    Homepage - Trang chủ cho user
    """
    return render(request, 'core/home.html')