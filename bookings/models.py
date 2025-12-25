from django.db import models
from django.utils import timezone
from users.models import User
from tours.models import Tour
from hotels.models import Hotel
from flight.models import Flight
from catalog.models import Package

class Booking(models.Model):
    """
    Model quản lý thông tin đặt chỗ
    """
    BOOKING_TYPES = [
        ('tour', 'Tour'),
        ('hotel', 'Hotel'),
        ('flight', 'Flight'),
    ]
    
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPES, verbose_name="Loại đặt chỗ")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tour")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Khách sạn")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Chuyến bay")
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Gói gợi ý")
    booking_date = models.DateField(verbose_name="Ngày đặt")
    number_of_people = models.IntegerField(verbose_name="Số người")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tổng giá")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='pending', verbose_name="Status")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'bookings_booking'
        verbose_name = "Đặt chỗ"
        verbose_name_plural = "Đặt chỗ"
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.full_name}"


class Ticket(models.Model):
    """
    Model quản lý vé sau khi thanh toán
    """
    ticket_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='ticket', verbose_name="Booking")
    passenger_name = models.CharField(max_length=255, verbose_name="Tên hành khách")
    flight_details = models.TextField(verbose_name="Chi tiết chuyến bay/xe bus", blank=True)
    hotel_room_details = models.TextField(verbose_name="Chi tiết phòng khách sạn", blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tổng chi phí")
    payment_method = models.CharField(max_length=50, verbose_name="Phương thức thanh toán", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        db_table = 'bookings_ticket'
        verbose_name = "Vé"
        verbose_name_plural = "Vé"
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.passenger_name}"
