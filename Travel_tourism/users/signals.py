"""
Signals - Xử lý tự động các sự kiện
Ví dụ: Gửi email chào mừng khi user đăng ký, log activity...
"""

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import User
from .services import EmailService
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Signal sau khi User được lưu
    - Nếu user mới được tạo: gửi email chào mừng
    - Log hoạt động
    """
    if created:
        # User mới được tạo
        logger.info(f"New user created: {instance.email} (ID: {instance.user_id})")
        
        # Gửi email chào mừng (chạy background để không block)
        try:
            EmailService.send_welcome_email(instance)
            logger.info(f"Welcome email sent to {instance.email}")
        except Exception as e:
            logger.error(f"Failed to send welcome email to {instance.email}: {e}")
    else:
        # User được cập nhật
        logger.info(f"User updated: {instance.email} (ID: {instance.user_id})")


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    """
    Signal trước khi User được lưu
    - Có thể dùng để validate thêm
    - Log changes
    """
    if instance.user_id:  # User đã tồn tại (đang update)
        try:
            old_user = User.objects.get(user_id=instance.user_id)
            
            # Log nếu role thay đổi
            if old_user.role != instance.role:
                logger.warning(
                    f"User role changed: {instance.email} "
                    f"from {old_user.role} to {instance.role}"
                )
            
            # Log nếu bị khóa/mở khóa
            if old_user.is_active != instance.is_active:
                status = "activated" if instance.is_active else "deactivated"
                logger.warning(f"User {status}: {instance.email}")
                
        except User.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def user_post_delete(sender, instance, **kwargs):
    """
    Signal sau khi User bị xóa
    - Log việc xóa user
    """
    logger.warning(
        f"User deleted: {instance.email} (ID: {instance.user_id})"
    )


# Optional: Custom signals nếu cần
from django.dispatch import Signal

# Signal tự định nghĩa
user_logged_in = Signal()  # Có thể dùng providing_args=['user', 'request']
user_logged_out = Signal()
user_password_changed = Signal()


@receiver(user_logged_in)
def on_user_login(sender, user, request, **kwargs):
    """
    Xử lý khi user đăng nhập
    - Log login
    - Có thể lưu last_login time
    - Track login location, device...
    """
    logger.info(f"User logged in: {user.email} from IP {request.META.get('REMOTE_ADDR')}")
    
    # Có thể lưu thông tin login
    # LoginHistory.objects.create(
    #     user=user,
    #     ip_address=request.META.get('REMOTE_ADDR'),
    #     user_agent=request.META.get('HTTP_USER_AGENT')
    # )


@receiver(user_logged_out)
def on_user_logout(sender, user, **kwargs):
    """Xử lý khi user đăng xuất"""
    logger.info(f"User logged out: {user.email if user else 'Unknown'}")


@receiver(user_password_changed)
def on_password_changed(sender, user, **kwargs):
    """
    Xử lý khi user đổi mật khẩu
    - Gửi email thông báo
    - Xóa tất cả session cũ (force re-login)
    """
    logger.info(f"Password changed for user: {user.email}")
    
    # Có thể gửi email cảnh báo
    # EmailService.send_password_changed_alert(user)