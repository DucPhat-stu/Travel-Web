from django.db import models
from django.utils import timezone

class Hotel(models.Model):
    """
    Model quản lý thông tin khách sạn
    """
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Tên khách sạn")
    description = models.TextField(verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    location = models.CharField(max_length=255, verbose_name="Địa điểm")
    amenities = models.TextField(verbose_name="Tiện nghi")
    image = models.ImageField(upload_to='hotels/', blank=True, null=True, verbose_name="Hình ảnh")
    rooms_available = models.PositiveIntegerField(default=0, verbose_name="Số phòng còn trống")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'hotels_hotel'
        verbose_name = "Khách sạn"
        verbose_name_plural = "Khách sạn"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
