"""
Unit tests cho module users
Chạy: python manage.py test users
"""

from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from .services import UserService, PasswordResetService, SessionService


class UserModelTest(TestCase):
    """Test User model"""
    
    def setUp(self):
        """Chuẩn bị dữ liệu test"""
        self.user = User(
            full_name='Test User',
            email='test@example.com',
            phone='0123456789',
            role='user'
        )
        self.user.set_password('testpass123')
        self.user.save()
    
    def test_user_creation(self):
        """Test tạo user"""
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.is_active)
    
    def test_password_hashing(self):
        """Test mật khẩu được hash"""
        self.assertNotEqual(self.user.password, 'testpass123')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.check_password('wrongpass'))
    
    def test_is_admin(self):
        """Test phân quyền"""
        self.assertFalse(self.user.is_admin())
        
        admin = User.objects.create(
            full_name='Admin',
            email='admin@example.com',
            phone='0987654321',
            role='admin'
        )
        self.assertTrue(admin.is_admin())
    
    def test_reset_token_generation(self):
        """Test tạo reset token"""
        token = self.user.generate_reset_token()
        self.assertIsNotNone(token)
        self.assertIsNotNone(self.user.reset_token)
        self.assertIsNotNone(self.user.reset_token_expiry)
    
    def test_reset_token_verification(self):
        """Test verify token"""
        token = self.user.generate_reset_token()
        self.assertTrue(self.user.verify_reset_token(token))
        self.assertFalse(self.user.verify_reset_token('wrong-token'))


class UserServiceTest(TestCase):
    """Test UserService"""
    
    def test_create_user(self):
        """Test tạo user qua service"""
        user = UserService.create_user(
            full_name='New User',
            email='newuser@example.com',
            phone='0123456789',
            password='password123'
        )
        
        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.email, 'newuser@example.com')
    
    def test_create_duplicate_email(self):
        """Test tạo user với email trùng"""
        UserService.create_user(
            full_name='User 1',
            email='same@example.com',
            phone='0123456789',
            password='pass123'
        )
        
        with self.assertRaises(ValueError):
            UserService.create_user(
                full_name='User 2',
                email='same@example.com',
                phone='0987654321',
                password='pass456'
            )
    
    def test_authenticate_user(self):
        """Test authenticate"""
        user = UserService.create_user(
            full_name='Auth User',
            email='auth@example.com',
            phone='0123456789',
            password='authpass123'
        )
        
        # Đúng password
        auth_user = UserService.authenticate_user('auth@example.com', 'authpass123')
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user.user_id, user.user_id)
        
        # Sai password
        auth_user = UserService.authenticate_user('auth@example.com', 'wrongpass')
        self.assertIsNone(auth_user)
        
        # Email không tồn tại
        auth_user = UserService.authenticate_user('notexist@example.com', 'anypass')
        self.assertIsNone(auth_user)


class PasswordResetServiceTest(TestCase):
    """Test PasswordResetService"""
    
    def setUp(self):
        self.user = UserService.create_user(
            full_name='Reset User',
            email='reset@example.com',
            phone='0123456789',
            password='oldpass123'
        )
    
    def test_request_password_reset(self):
        """Test yêu cầu reset password"""
        success, token = PasswordResetService.request_password_reset('reset@example.com')
        
        self.assertTrue(success)
        self.assertIsNotNone(token)
    
    def test_verify_reset_token(self):
        """Test verify token"""
        success, token = PasswordResetService.request_password_reset('reset@example.com')
        
        user = PasswordResetService.verify_reset_token('reset@example.com', token)
        self.assertIsNotNone(user)
        
        # Wrong token
        user = PasswordResetService.verify_reset_token('reset@example.com', 'wrong')
        self.assertIsNone(user)
    
    def test_reset_password(self):
        """Test reset password"""
        success, token = PasswordResetService.request_password_reset('reset@example.com')
        user = PasswordResetService.verify_reset_token('reset@example.com', token)
        
        PasswordResetService.reset_password(user, 'newpass456')
        
        # Kiểm tra password mới
        auth_user = UserService.authenticate_user('reset@example.com', 'newpass456')
        self.assertIsNotNone(auth_user)
        
        # Password cũ không dùng được
        auth_user = UserService.authenticate_user('reset@example.com', 'oldpass123')
        self.assertIsNone(auth_user)


class AuthViewTest(TestCase):
    """Test authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserService.create_user(
            full_name='View Test User',
            email='viewtest@example.com',
            phone='0123456789',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test GET login page"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_login_success(self):
        """Test login thành công"""
        response = self.client.post(reverse('users:login'), {
            'email': 'viewtest@example.com',
            'password': 'testpass123'
        })
        
        # Should redirect
        self.assertEqual(response.status_code, 302)
        
        # Session should be created
        self.assertIn('user_id', self.client.session)
    
    def test_login_wrong_password(self):
        """Test login sai password"""
        response = self.client.post(reverse('users:login'), {
            'email': 'viewtest@example.com',
            'password': 'wrongpass'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('user_id', self.client.session)
    
    def test_register_view_get(self):
        """Test GET register page"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        """Test logout"""
        # Login first
        self.client.post(reverse('users:login'), {
            'email': 'viewtest@example.com',
            'password': 'testpass123'
        })
        
        # Then logout
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('user_id', self.client.session)


# Chạy test:
# python manage.py test users
# python manage.py test users.tests.UserModelTest
# python manage.py test users.tests.UserServiceTest