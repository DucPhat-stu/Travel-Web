"""
Services - Business Logic Layer
Tách logic nghiệp vụ ra khỏi views để dễ test và tái sử dụng
"""

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import User
from typing import Optional, Dict, Tuple


class UserService:
    """Service xử lý logic liên quan đến User"""
    
    @staticmethod
    def create_user(
        full_name: str,
        email: str,
        phone: str,
        password: str,
        address: str = '',
        role: str = 'user'
    ) -> User:
        """
        Tạo user mới
        
        Returns:
            User object
        Raises:
            ValueError: Nếu email đã tồn tại
        """
        if User.objects.filter(email=email).exists():
            raise ValueError('Email đã được sử dụng!')
        
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            role=role
        )
        user.set_password(password)
        user.save()
        
        return user
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        """
        Xác thực user
        
        Returns:
            User nếu thành công, None nếu thất bại
        """
        try:
            user = User.objects.get(email=email)
            
            if not user.is_active:
                return None
            
            if user.check_password(password):
                return user
            
        except User.DoesNotExist:
            pass
        
        return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Lấy user theo ID"""
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Lấy user theo email"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def update_user(
        user: User,
        full_name: str = None,
        phone: str = None,
        address: str = None
    ) -> User:
        """Cập nhật thông tin user"""
        if full_name:
            user.full_name = full_name
        if phone:
            user.phone = phone
        if address is not None:
            user.address = address
        
        user.save()
        return user
    
    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> bool:
        """
        Đổi mật khẩu
        
        Returns:
            True nếu thành công, False nếu mật khẩu cũ sai
        """
        if not user.check_password(old_password):
            return False
        
        user.set_password(new_password)
        user.save()
        return True
    
    @staticmethod
    def deactivate_user(user: User) -> None:
        """Vô hiệu hóa tài khoản"""
        user.is_active = False
        user.save()
    
    @staticmethod
    def activate_user(user: User) -> None:
        """Kích hoạt lại tài khoản"""
        user.is_active = True
        user.save()


class PasswordResetService:
    """Service xử lý logic reset mật khẩu"""
    
    @staticmethod
    def request_password_reset(email: str) -> Tuple[bool, Optional[str]]:
        """
        Yêu cầu reset mật khẩu
        
        Returns:
            (success: bool, token: str hoặc None)
        """
        try:
            user = User.objects.get(email=email)
            token = user.generate_reset_token()
            return True, token
        except User.DoesNotExist:
            return False, None
    
    @staticmethod
    def verify_reset_token(email: str, token: str) -> Optional[User]:
        """
        Kiểm tra token có hợp lệ không
        
        Returns:
            User nếu token hợp lệ, None nếu không
        """
        try:
            user = User.objects.get(email=email)
            if user.verify_reset_token(token):
                return user
        except User.DoesNotExist:
            pass
        
        return None
    
    @staticmethod
    def reset_password(user: User, new_password: str) -> None:
        """Reset mật khẩu và xóa token"""
        user.set_password(new_password)
        user.clear_reset_token()


class EmailService:
    """Service gửi email"""
    
    @staticmethod
    def send_password_reset_email(
        user: User,
        reset_link: str
    ) -> bool:
        """
        Gửi email reset password
        
        Returns:
            True nếu gửi thành công, False nếu thất bại
        """
        subject = 'Khôi phục mật khẩu - Travel Tourism'
        message = f"""
Xin chào {user.full_name},

Bạn đã yêu cầu khôi phục mật khẩu cho tài khoản {user.email}.

Vui lòng nhấn vào link sau để đặt lại mật khẩu:
{reset_link}

Link này có hiệu lực trong 24 giờ.

Nếu bạn không yêu cầu khôi phục mật khẩu, vui lòng bỏ qua email này.

Trân trọng,
Travel Tourism Team
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    @staticmethod
    def send_welcome_email(user: User) -> bool:
        """
        Gửi email chào mừng sau khi đăng ký
        
        Returns:
            True nếu gửi thành công
        """
        subject = 'Chào mừng đến với Travel Tourism'
        message = f"""
Xin chào {user.full_name},

Cảm ơn bạn đã đăng ký tài khoản tại Travel Tourism!

Thông tin tài khoản:
- Email: {user.email}
- Số điện thoại: {user.phone}

Bạn có thể bắt đầu khám phá các tour du lịch, khách sạn và chuyến bay ngay bây giờ.

Chúc bạn có những trải nghiệm tuyệt vời!

Trân trọng,
Travel Tourism Team
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,  # Không fail nếu gửi email lỗi
            )
            return True
        except Exception as e:
            print(f"Welcome email error: {e}")
            return False


class SessionService:
    """Service quản lý session"""
    
    @staticmethod
    def create_session(request, user: User) -> None:
        """Tạo session cho user sau khi login"""
        request.session['user_id'] = user.user_id
        request.session['user_email'] = user.email
        request.session['user_name'] = user.full_name
        request.session['user_role'] = user.role
        request.session['login_time'] = timezone.now().isoformat()
    
    @staticmethod
    def clear_session(request) -> None:
        """Xóa session khi logout"""
        request.session.flush()
    
    @staticmethod
    def get_current_user(request) -> Optional[User]:
        """Lấy user hiện tại từ session"""
        user_id = request.session.get('user_id')
        if user_id:
            return UserService.get_user_by_id(user_id)
        return None
    
    @staticmethod
    def is_authenticated(request) -> bool:
        """Kiểm tra user đã đăng nhập chưa"""
        return request.session.get('user_id') is not None
    
    @staticmethod
    def is_admin(request) -> bool:
        """Kiểm tra user có phải admin không"""
        return request.session.get('user_role') == 'admin'


class UserStatisticsService:
    """Service thống kê user (dùng cho admin)"""
    
    @staticmethod
    def get_total_users() -> int:
        """Tổng số user"""
        return User.objects.count()
    
    @staticmethod
    def get_active_users_count() -> int:
        """Số user đang hoạt động"""
        return User.objects.filter(is_active=True).count()
    
    @staticmethod
    def get_admin_users_count() -> int:
        """Số admin"""
        return User.objects.filter(role='admin').count()
    
    @staticmethod
    def get_new_users_today() -> int:
        """Số user đăng ký hôm nay"""
        today = timezone.now().date()
        return User.objects.filter(created_at__date=today).count()
    
    @staticmethod
    def get_new_users_this_week() -> int:
        """Số user đăng ký tuần này"""
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        return User.objects.filter(created_at__gte=week_ago).count()
    
    @staticmethod
    def get_new_users_this_month() -> int:
        """Số user đăng ký tháng này"""
        from datetime import timedelta
        month_ago = timezone.now() - timedelta(days=30)
        return User.objects.filter(created_at__gte=month_ago).count()
    
    @staticmethod
    def get_user_statistics() -> Dict:
        """Lấy tất cả thống kê"""
        return {
            'total_users': UserStatisticsService.get_total_users(),
            'active_users': UserStatisticsService.get_active_users_count(),
            'admin_users': UserStatisticsService.get_admin_users_count(),
            'new_today': UserStatisticsService.get_new_users_today(),
            'new_this_week': UserStatisticsService.get_new_users_this_week(),
            'new_this_month': UserStatisticsService.get_new_users_this_month(),
        }