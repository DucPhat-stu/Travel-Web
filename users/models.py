from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

class User(AbstractBaseUser, PermissionsMixin):
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

    # Profile fields
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Ảnh đại diện")
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="Giới thiệu")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name="Giới tính")

    # Thêm các trường hỗ trợ
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    is_staff = models.BooleanField(default=False, verbose_name="Nhân viên")
    is_superuser = models.BooleanField(default=False, verbose_name="Siêu người dùng")
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="Lần đăng nhập cuối")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    # Cho chức năng reset password
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expiry = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:

        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def get_full_name(self):
        """Compatibility helper: return the user's full name or email."""
        return self.full_name or self.email

    def get_short_name(self):
        """Compatibility helper: return first name or email if not available."""
        if self.full_name:
            parts = self.full_name.split()
            if parts:
                return parts[0]
        return self.email

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

    @property
    def is_authenticated(self):
        """
        Thuộc tính dùng cho DRF/Django permissions.
        Luôn True khi user được load từ token/session hợp lệ.
        """
        return True

    @property
    def is_anonymous(self):
        return False

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        Simplest possible answer: Yes, always for superusers
        """
        return self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """
        Does the user have each of the specified permissions?
        Simplest possible answer: Yes, always for superusers
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        Simplest possible answer: Yes, always for superusers
        """
        return self.is_superuser


class UserPost(models.Model):
    """
    Model lưu trữ các bài đăng/hình ảnh trải nghiệm của user
    Giống như Instagram wall/feed
    """
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Người dùng")
    image = models.ImageField(upload_to='user_posts/', verbose_name="Hình ảnh")
    caption = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Mô tả")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Địa điểm")
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        blank=True,
        null=True,
        verbose_name="Đánh giá (1-5 sao)"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Bình luận")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'users_user_post'
        verbose_name = "Bài đăng"
        verbose_name_plural = "Bài đăng"
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.full_name} at {self.created_at}"


class UserToken(models.Model):
    """
    Token xác thực cho API.
    Lưu để có thể thu hồi và kiểm soát phiên làm việc.
    """
    key = models.CharField(max_length=40, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users_user_token'
        verbose_name = "API Token"
        verbose_name_plural = "API Tokens"
        ordering = ['-created_at']

    def __str__(self):
        return f"Token for {self.user.email}"
