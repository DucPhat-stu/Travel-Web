from django.db import models
from django.utils import timezone

class Flight(models.Model):
    """
    Model quản lý thông tin chuyến bay
    """
    flight_id = models.AutoField(primary_key=True)
    flight_number = models.CharField(max_length=10, verbose_name="Số hiệu chuyến bay")
    departure = models.CharField(max_length=255, verbose_name="Điểm khởi hành")
    destination = models.CharField(max_length=255, verbose_name="Điểm đến")
    departure_time = models.DateTimeField(verbose_name="Thời gian khởi hành")
    arrival_time = models.DateTimeField(verbose_name="Thời gian đến")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    airline = models.CharField(max_length=255, verbose_name="Hãng hàng không")
    seats_available = models.PositiveIntegerField(default=0, verbose_name="Số ghế còn trống")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'flight_flight'
        verbose_name = "Chuyến bay"
        verbose_name_plural = "Chuyến bay"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.flight_number} - {self.departure} to {self.destination}"
