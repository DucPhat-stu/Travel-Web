from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class AuthMiddleware:
    """
    Middleware kiểm tra authentication và phân quyền
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Các URL không cần đăng nhập
        self.public_urls = [
            '/users/login/',
            '/users/register/',
            '/users/forget/',
            '/users/reset/',
            '/static/',
            '/',  # Homepage
        ]
        
        # Các URL chỉ admin mới truy cập được
        self.admin_urls = [
            '/admin-panel/',
        ]
    
    def __call__(self, request):
        path = request.path
        
        # Bỏ qua các URL public
        if any(path.startswith(url) for url in self.public_urls):
            response = self.get_response(request)
            return response
        
        # Kiểm tra đã đăng nhập chưa
        user_id = request.session.get('user_id')
        
        if not user_id:
            messages.warning(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('users:login')
        
        # Kiểm tra quyền admin cho admin URLs
        if any(path.startswith(url) for url in self.admin_urls):
            user_role = request.session.get('user_role')
            if user_role != 'admin':
                messages.error(request, 'Bạn không có quyền truy cập trang này!')
                return redirect('core:home')
        
        response = self.get_response(request)
        return response


class LoginRequiredMixin:
    """
    Mixin để bảo vệ view, yêu cầu đăng nhập
    Sử dụng: class MyView(LoginRequiredMixin, View)
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:
    """
    Mixin để bảo vệ view, yêu cầu quyền admin
    Sử dụng: class AdminView(AdminRequiredMixin, View)
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('users:login')
        
        if request.session.get('user_role') != 'admin':
            messages.error(request, 'Bạn không có quyền truy cập trang này!')
            return redirect('core:home')
        
        return super().dispatch(request, *args, **kwargs)