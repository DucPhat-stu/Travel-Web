from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Tạo tài khoản admin mặc định'

    def handle(self, *args, **options):
        # Kiểm tra admin đã tồn tại chưa
        if User.objects.filter(email='admin@travel.com').exists():
            self.stdout.write(
                self.style.WARNING('Admin đã tồn tại!')
            )
            return
        
        # Tạo admin mới
        admin = User(
            full_name='Administrator',
            email='admin@travel.com',
            phone='0123456789',
            address='Ha Noi, Vietnam',
            role='admin'
        )
        admin.set_password('admin123')
        admin.save()
        
        self.stdout.write(
            self.style.SUCCESS('✓ Tạo admin thành công!')
        )
        self.stdout.write('Email: admin@travel.com')
        self.stdout.write('Password: admin123')