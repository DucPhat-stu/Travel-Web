from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from tours.models import Tour
from hotels.models import Hotel
from flight.models import Flight


class Destination(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=120, blank=True)
    region = models.CharField(max_length=120, blank=True)
    best_season = models.CharField(max_length=120, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="CSV tags, vd: beach,adventure,family")
    hero_image = models.ImageField(upload_to="destinations/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_destination"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Package(models.Model):
    LABEL_CHOICES = [
        ("family", "Gia đình"),
        ("couple", "Cặp đôi"),
        ("adventure", "Phiêu lưu"),
        ("luxury", "Cao cấp"),
        ("budget", "Tiết kiệm"),
    ]

    title = models.CharField(max_length=255)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="packages")
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    label = models.CharField(max_length=50, choices=LABEL_CHOICES, blank=True)
    rating_cached = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tours = models.ManyToManyField(Tour, blank=True, related_name="packages")
    hotels = models.ManyToManyField(Hotel, blank=True, related_name="packages")
    flights = models.ManyToManyField(Flight, blank=True, related_name="packages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_package"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(models.Model):
    STATUS_CHOICES = [
        ("pending", "Chờ duyệt"),
        ("approved", "Đã duyệt"),
        ("rejected", "Từ chối"),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "catalog_review"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.rating}"


class Comment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Chờ duyệt"),
        ("approved", "Đã duyệt"),
        ("rejected", "Từ chối"),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "catalog_comment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.email}"


class AirlineFareRule(models.Model):
    CARRIER_CHOICES = [
        ("vietjet", "VietJet Air"),
        ("bamboo", "Bamboo Airways"),
        ("vna", "Vietnam Airlines"),
        ("viettravel", "Vietravel Airlines"),
    ]
    ROUTE_CHOICES = [
        ("domestic", "Nội địa"),
        ("international", "Quốc tế"),
    ]
    TRIP_CHOICES = [
        ("oneway", "Một chiều"),
        ("roundtrip", "Khứ hồi"),
    ]

    carrier = models.CharField(max_length=20, choices=CARRIER_CHOICES)
    route_type = models.CharField(max_length=20, choices=ROUTE_CHOICES)
    trip_type = models.CharField(max_length=20, choices=TRIP_CHOICES)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    multiplier_advance = models.DecimalField(
        max_digits=6, decimal_places=4, default=0.01, help_text="Hệ số tăng theo số ngày đặt trước"
    )
    tax_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="VND")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "catalog_airlinefarerule"
        unique_together = ("carrier", "route_type", "trip_type")

    def __str__(self):
        return f"{self.carrier} - {self.route_type} - {self.trip_type}"


class VisaRequirement(models.Model):
    country_code = models.CharField(max_length=5, unique=True)
    visa_required = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = "catalog_visarequirement"

    def __str__(self):
        return f"{self.country_code} - {'Visa' if self.visa_required else 'No Visa'}"

