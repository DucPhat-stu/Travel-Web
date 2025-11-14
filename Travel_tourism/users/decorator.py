from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_func):
    """
    Decorator yêu cầu đăng nhập
    
    Sử dụng:
    @login_required
    def my_view(request):
        ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Decorator yêu cầu quyền admin
    
    Sử dụng:
    @admin_required
    def admin_view(request):
        ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('users:login')
        
        if request.session.get('user_role') != 'admin':
            messages.error(request, 'Bạn không có quyền truy cập trang này!')
            return redirect('core:home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def anonymous_required(view_func):
    """
    Decorator yêu cầu chưa đăng nhập (dùng cho login/register page)
    Nếu đã login thì redirect về home
    
    Sử dụng:
    @anonymous_required
    def login_view(request):
        ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id'):
            user_role = request.session.get('user_role')
            if user_role == 'admin':
                return redirect('admin_panel:dashboard')
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return wrapper