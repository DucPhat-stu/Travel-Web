# Module Users - Authentication & Authorization

##  Chức năng đã hoàn thành

###  Backend
- [x] Model User với các trường cần thiết
- [x] Đăng ký tài khoản (U01)
- [x] Đăng nhập (U02)
- [x] Đăng xuất (U03)
- [x] Quên mật khẩu (U04)
- [x] Reset mật khẩu (U04)
- [x] Phân quyền user/admin
- [x] Redirect sau login theo role
- [x] Middleware bảo vệ routes
- [x] Decorators tiện ích
- [x] Context processor cho templates

---

##  Hướng dẫn cài đặt

### 1. Tạo migrations
```bash
python manage.py makemigrations users
python manage.py migrate
```

### 2. Tạo tài khoản admin mặc định
```bash
python manage.py create_admin
```

**Thông tin đăng nhập admin:**
- Email: `admin@travel.com`
- Password: `admin123`

### 3. Chạy server
```bash
python manage.py runserver
```

---

##  API Endpoints

| Method | Endpoint | Chức năng | Quyền truy cập |
|--------|----------|-----------|----------------|
| GET/POST | `/users/register/` | Đăng ký tài khoản | Public |
| GET/POST | `/users/login/` | Đăng nhập | Public |
| GET/POST | `/users/logout/` | Đăng xuất | Authenticated |
| GET/POST | `/users/forget/` | Quên mật khẩu | Public |
| GET/POST | `/users/reset/?token=xxx&email=xxx` | Reset mật khẩu | Public |

---

##  Sử dụng trong Views

### 1. Sử dụng Decorators

```python
from users.decorators import login_required, admin_required

@login_required
def my_view(request):
    # Chỉ user đã login mới vào được
    user_id = request.session['user_id']
    return render(request, 'my_template.html')

@admin_required
def admin_view(request):
    # Chỉ admin mới vào được
    return render(request, 'admin_template.html')
```

### 2. Sử dụng Mixins (Class-based views)

```python
from users.middleware import LoginRequiredMixin, AdminRequiredMixin
from django.views import View

class MyView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'my_template.html')

class AdminView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_template.html')
```

### 3. Lấy thông tin user trong view

```python
def my_view(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    user_role = request.session.get('user_role')
    
    # Hoặc lấy từ database
    from users.models import User
    user = User.objects.get(user_id=user_id)
```

---

##  Sử dụng trong Templates

### 1. Kiểm tra đăng nhập

```django
{% if current_user.is_authenticated %}
    <p>Xin chào, {{ current_user.name }}!</p>
    <a href="{% url 'users:logout' %}">Đăng xuất</a>
{% else %}
    <a href="{% url 'users:login' %}">Đăng nhập</a>
    <a href="{% url 'users:register' %}">Đăng ký</a>
{% endif %}
```

### 2. Kiểm tra quyền admin

```django
{% if current_user.is_admin %}
    <a href="{% url 'admin_panel:dashboard' %}">Quản trị</a>
{% endif %}
```

---

##  Database Schema

```sql
CREATE TABLE users_user (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(500),
    role VARCHAR(10) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reset_token VARCHAR(100),
    reset_token_expiry TIMESTAMP
);
```

---

##  Cấu hình Email (cho chức năng quên mật khẩu)

### Development (in ra console)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production (Gmail)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Tạo App Password trong Gmail
DEFAULT_FROM_EMAIL = 'noreply@travel-tourism.com'
```

---

##  Test thử nghiệm

### 1. Test đăng ký
```bash
curl -X POST http://localhost:8000/users/register/ \
  -d "full_name=Test User" \
  -d "email=test@example.com" \
  -d "phone=0123456789" \
  -d "password=test12345" \
  -d "confirm_password=test12345"
```

### 2. Test đăng nhập
```bash
curl -X POST http://localhost:8000/users/login/ \
  -d "email=admin@travel.com" \
  -d "password=admin123"
```

---

##  TO DO - Frontend (Member 2)

Cần tạo các template sau:

1. **templates/users/register.html** - Form đăng ký
2. **templates/users/login.html** - Form đăng nhập
3. **templates/users/forget_password.html** - Form quên mật khẩu
4. **templates/users/reset_password.html** - Form reset mật khẩu
5. **templates/core/home.html** - Trang chủ user

Các template cần hiển thị:
- Form với các field tương ứng
- Messages (success/error/warning)
- Validation errors

---

##  Bảo mật

-  Mật khẩu được hash bằng Django's password hasher
-  CSRF protection
-  Session-based authentication
-  Reset token có thời hạn 24 giờ
-  Middleware kiểm tra quyền truy cập
-  Validation email/phone/password

---

##  Liên hệ

- **Member 1**: Backend Auth
- **Thời gian hoàn thành**: Tuần 1
- **Status**:  Hoàn thành backend, đợi frontend tích hợp