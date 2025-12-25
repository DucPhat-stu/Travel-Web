"""
Context processors để inject user vào template context
"""
from .services import SessionService


def user_context(request):
    """
    Thêm thông tin user vào context của tất cả templates
    """
    user = SessionService.get_current_user(request)
    
    return {
        'user': user,
        'is_authenticated': SessionService.is_authenticated(request),
        'is_admin': SessionService.is_admin(request),
    }