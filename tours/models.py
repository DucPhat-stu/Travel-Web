from django.db import models
from django.utils import timezone

class Tour(models.Model):
    """
    Model quản lý thông tin tour du lịch
    """
    tour_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Tên tour")
    description = models.TextField(verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    duration = models.IntegerField(verbose_name="Số ngày")
    location = models.CharField(max_length=255, verbose_name="Địa điểm")
    image = models.ImageField(upload_to='tours/', blank=True, null=True, verbose_name="Hình ảnh")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'tours_tour'
        verbose_name = "Tour"
        verbose_name_plural = "Tour"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
