from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from users.authentication import UserTokenAuthentication
from tours.models import Tour
from catalog.models import Destination, Package
from bookings.models import Booking


class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            full_name="User A",
            email="user@example.com",
            phone="0123",
            address="HN",
            role="user",
            password="",
            is_active=True,
        )
        self.user.set_password("password123")
        self.user.save()
        self.token = UserTokenAuthentication.issue_token(self.user)

        self.destination = Destination.objects.create(
            name="Ha Long",
            slug="ha-long",
            country="VN",
            region="Quang Ninh",
        )

        self.tour = Tour.objects.create(
            name="Ha Long",
            description="Vịnh Hạ Long",
            price=500,
            duration=3,
            location="Quang Ninh",
            is_active=True,
        )
        self.package = Package.objects.create(
            title="Gói Ha Long 3N2Đ",
            destination=self.destination,
            description="Gói combo",
            base_price=1500,
            label="family",
            is_active=True,
        )
        self.package.tours.add(self.tour)

    def auth_headers(self):
        return {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

    def test_create_booking_requires_token(self):
        url = reverse("api:booking-list")
        payload = {
            "booking_type": "tour",
            "tour": self.tour.pk,
            "booking_date": "2024-01-01",
            "number_of_people": 2,
            "total_price": "1000.00",
        }
        resp = self.client.post(url, payload)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_success(self):
        url = reverse("api:booking-list")
        payload = {
            "booking_type": "tour",
            "tour": self.tour.pk,
            "package": self.package.pk,
            "booking_date": "2024-01-01",
            "number_of_people": 2,
            "total_price": "1000.00",
        }
        resp = self.client.post(url, payload, **self.auth_headers())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)

    def test_validation_requires_matching_object(self):
        url = reverse("api:booking-list")
        payload = {
            "booking_type": "hotel",
            "tour": self.tour.pk,
            "booking_date": "2024-01-01",
            "number_of_people": 1,
            "total_price": "100.00",
        }
        resp = self.client.post(url, payload, **self.auth_headers())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Phải chọn hotel", str(resp.data))

