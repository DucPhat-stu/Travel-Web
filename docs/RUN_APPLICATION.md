# Hướng Dẫn Chạy Ứng Dụng (Run Application Guide)

## 🚀 Bắt Đầu Nhanh (5 Phút)

### Bước 1: Chuẩn Bị (1 phút)

```bash
# Vào thư mục dự án
cd "c:\Users\Phat\OneDrive\Máy tính\travel-web\Travel-Web"

# Kiểm tra Python
python --version

# Kiểm tra PostgreSQL
psql --version
```

### Bước 2: Cài Đặt Dependencies (1 phút)

```bash
# Cài đặt requirements
pip install -r requirements.txt
```

### Bước 3: Cấu Hình Database (1 phút)

```bash
# Tạo migration
python manage.py makemigrations

# Áp dụng migration
python manage.py migrate

# Tạo superuser (admin)
python manage.py createsuperuser
# Nhập: admin / admin@example.com / password123
```

### Bước 4: Chạy Server (1 phút)

```bash
# Chạy development server
python manage.py runserver
```

### Bước 5: Truy Cập (1 phút)

```
Trang chủ: http://localhost:8000/
Đăng kí: http://localhost:8000/users/register/
Đăng nhập: http://localhost:8000/users/login/
Admin: http://localhost:8000/django-admin/
```

---

## 📋 Chi Tiết Từng Bước

### Bước 1: Kiểm Tra Yêu Cầu

#### Python
```bash
python --version
# Kết quả: Python 3.8+
```

#### PostgreSQL
```bash
psql --version
# Kết quả: psql (PostgreSQL) 12+
```

#### Git
```bash
git --version
# Kết quả: git version 2.x+
```

### Bước 2: Clone/Mở Dự Án

```bash
# Nếu chưa có dự án
git clone <repository-url>

# Vào thư mục dự án
cd Travel-Web
```

### Bước 3: Tạo Virtual Environment (Tùy Chọn)

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (Mac/Linux)
source venv/bin/activate
```

### Bước 4: Cài Đặt Dependencies

```bash
# Cài đặt từ requirements.txt
pip install -r requirements.txt

# Hoặc cài đặt thủ công
pip install django
pip install djangorestframework
pip install psycopg2-binary
pip install python-dotenv
```

### Bước 5: Cấu Hình Database

#### Kiểm Tra PostgreSQL

```bash
# Kết nối đến PostgreSQL
psql -U postgres

# Trong PostgreSQL shell:
# Tạo database
CREATE DATABASE travel_tourism_db;

# Tạo user (nếu chưa có)
CREATE USER postgres WITH PASSWORD 'postgres';

# Cấp quyền
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET default_transaction_deferrable TO on;
ALTER ROLE postgres SET default_transaction_level TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE travel_tourism_db TO postgres;

# Thoát
\q
```

#### Kiểm Tra .env

```bash
# Kiểm tra file .env
cat .env

# Nội dung:
POSTGRES_DB=travel_tourism_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DEBUG=True
```

#### Chạy Migration

```bash
# Tạo migration files
python manage.py makemigrations

# Áp dụng migration
python manage.py migrate

# Kiểm tra trạng thái
python manage.py showmigrations
```

### Bước 6: Tạo Superuser

```bash
# Tạo superuser
python manage.py createsuperuser

# Nhập thông tin:
# Username: admin
# Email: admin@example.com
# Password: password123
# Password (again): password123
```

### Bước 7: Chạy Server

```bash
# Chạy development server
python manage.py runserver

# Hoặc chạy trên port khác
python manage.py runserver 8001

# Hoặc chạy trên IP khác
python manage.py runserver 0.0.0.0:8000
```

### Bước 8: Truy Cập Ứng Dụng

```
Trang chủ: http://localhost:8000/
Đăng kí: http://localhost:8000/users/register/
Đăng nhập: http://localhost:8000/users/login/
Admin: http://localhost:8000/django-admin/
API: http://localhost:8000/api/
```

---

## 🔍 Kiểm Tra Kết Nối

### Kiểm Tra Database

```bash
# Mở Django shell
python manage.py shell

# Kiểm tra kết nối
from django.db import connection
connection.ensure_connection()
print("Database connected!")

# Kiểm tra bảng users
from users.models import User
print(f"Total users: {User.objects.count()}")

# Thoát
exit()
```

### Kiểm Tra Server

```bash
# Truy cập trang chủ
curl http://localhost:8000/

# Hoặc mở browser
http://localhost:8000/
```

---

## 📊 Xem Database

### Sử Dụng Django Admin

```
1. Truy cập: http://localhost:8000/django-admin/
2. Đăng nhập: admin / password123
3. Xem bảng Users
```

### Sử Dụng Django Shell

```bash
python manage.py shell

# Xem tất cả users
from users.models import User
for user in User.objects.all():
    print(f"{user.user_id}: {user.full_name} ({user.email})")

# Xem user cụ thể
user = User.objects.get(email='admin@example.com')
print(user)

# Thoát
exit()
```

### Sử Dụng PostgreSQL CLI

```bash
# Kết nối
psql -U postgres -d travel_tourism_db

# Xem tất cả users
SELECT * FROM users_user;

# Thoát
\q
```

---

## 🧪 Kiểm Tra Chức Năng

### Kiểm Tra Đăng Kí

```
1. Truy cập: http://localhost:8000/users/register/
2. Nhập thông tin:
   - Full Name: John Doe
   - Email: john@example.com
   - Phone: 0123456789
   - Password: password123
   - Confirm Password: password123
   - Address: 123 Main St
3. Click "Đăng Kí"
4. Kiểm tra database:
   python manage.py shell
   from users.models import User
   user = User.objects.get(email='john@example.com')
   print(user)
```

### Kiểm Tra Đăng Nhập

```
1. Truy cập: http://localhost:8000/users/login/
2. Nhập thông tin:
   - Email: john@example.com
   - Password: password123
3. Click "Đăng Nhập"
4. Kiểm tra session được tạo
```

### Kiểm Tra Đăng Xuất

```
1. Sau khi đăng nhập, click "Logout"
2. Kiểm tra session bị xóa
```

---

## 🛠️ Troubleshooting

### Lỗi: `could not connect to server`

**Nguyên nhân:** PostgreSQL không chạy

**Giải pháp:**
```bash
# Kiểm tra PostgreSQL
psql -U postgres

# Nếu lỗi, khởi động PostgreSQL
# Windows: Services → PostgreSQL → Start
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

### Lỗi: `No such table: users_user`

**Nguyên nhân:** Migration chưa được áp dụng

**Giải pháp:**
```bash
python manage.py migrate
```

### Lỗi: `ModuleNotFoundError: No module named 'django'`

**Nguyên nhân:** Dependencies chưa được cài đặt

**Giải pháp:**
```bash
pip install -r requirements.txt
```

### Lỗi: `Port 8000 already in use`

**Nguyên nhân:** Port 8000 đang được sử dụng

**Giải pháp:**
```bash
# Chạy trên port khác
python manage.py runserver 8001

# Hoặc tìm process sử dụng port 8000
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000
```

---

## 📝 Lệnh Hữu Ích

### Django Management

```bash
# Tạo migration
python manage.py makemigrations

# Áp dụng migration
python manage.py migrate

# Tạo superuser
python manage.py createsuperuser

# Chạy server
python manage.py runserver

# Mở Django shell
python manage.py shell

# Kết nối database
python manage.py dbshell

# Kiểm tra cấu hình
python manage.py check

# Xem tất cả URL
python manage.py show_urls

# Xem migration status
python manage.py showmigrations

# Xóa migration
python manage.py migrate <app> zero
```

### Database

```bash
# Kết nối PostgreSQL
psql -U postgres -d travel_tourism_db

# Xem tất cả bảng
\dt

# Xem chi tiết bảng
\d users_user

# Xem tất cả users
SELECT * FROM users_user;

# Thoát
\q
```

---

## 🎯 Checklist

- [ ] Python 3.8+ cài đặt
- [ ] PostgreSQL cài đặt và chạy
- [ ] Dependencies cài đặt
- [ ] Database tạo
- [ ] Migration áp dụng
- [ ] Superuser tạo
- [ ] Server chạy
- [ ] Trang chủ truy cập được
- [ ] Đăng kí hoạt động
- [ ] Đăng nhập hoạt động
- [ ] Admin truy cập được

---

## 🚀 Triển Khai Production

### Chuẩn Bị

```bash
# Cập nhật settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# Tạo secret key mới
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

# Cập nhật .env
SECRET_KEY=<new-secret-key>
DEBUG=False
```

### Chạy

```bash
# Collect static files
python manage.py collectstatic

# Chạy server production
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra `DATABASE_AND_AUTH_GUIDE.md`
2. Kiểm tra `BUTTON_SYSTEM_README.md`
3. Kiểm tra logs: `python manage.py runserver`

---

**Phiên bản:** 1.0  
**Ngày cập nhật:** 2024  
**Tác giả:** Development Team
