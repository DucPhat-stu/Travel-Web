from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class User(models.Model):
    """
    Model quản lý thông tin người dùng
    Bảng: users_user
    """
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, verbose_name="Họ tên")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    password = models.CharField(max_length=255, verbose_name="Mật khẩu")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Địa chỉ")
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='user',
        verbose_name="Vai trò"
    )
    
    # Thêm các trường hỗ trợ
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    # Cho chức năng reset password
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expiry = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'users_user'
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    def set_password(self, raw_password):
        """Mã hóa và lưu mật khẩu"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Kiểm tra mật khẩu"""
        return check_password(raw_password, self.password)
    
    def is_admin(self):
        """Kiểm tra có phải admin không ?"""
        return self.role == 'admin'
    
    def generate_reset_token(self):
        """Tạo token reset password"""
        import secrets
        from datetime import timedelta
        
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = timezone.now() + timedelta(hours=24)
        self.save()
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Kiểm tra token reset còn hợp lệ không"""
        if not self.reset_token or not self.reset_token_expiry:
            return False
        
        if self.reset_token != token:
            return False
        
        if timezone.now() > self.reset_token_expiry:
            return False
        
        return True
    
    def clear_reset_token(self):
        """Xóa token sau khi reset thành công"""
        self.reset_token = None
        self.reset_token_expiry = None
        self.save()